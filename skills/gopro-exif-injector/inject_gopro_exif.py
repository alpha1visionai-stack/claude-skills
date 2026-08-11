import os
import sys
import argparse
import subprocess
import re
import json
import sqlite3
from datetime import datetime
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

NIK_DB_PATH = r"C:\Users\walte\AppData\Local\DxO\Nik Collection 7\data.db"
NIK_EXE_PATH = r"C:\Program Files\DxO\Nik Collection 7\bin\Nik 7 Color Efex.exe"
SILVER_EFEX_EXE_PATH = r"C:\Program Files\DxO\Nik Collection 7\bin\Nik 7 Silver Efex.exe"

def find_exiftool():
    """Finds exiftool executable path on the system."""
    import shutil
    p = shutil.which("exiftool")
    if p:
        return p
    
    candidate_paths = [
        r"C:\Program Files\Skylum\Luminar Neo\exiftool.exe",
        r"C:\Program Files\exiftool\exiftool.exe",
        r"C:\Program Files (x86)\exiftool\exiftool.exe",
        r"C:\ProgramData\chocolatey\bin\exiftool.exe",
        os.path.expanduser(r"~\scoop\shims\exiftool.exe"),
        r"C:\Users\walte\AppData\Local\Programs\exiftool\exiftool.exe"
    ]
    for cp in candidate_paths:
        if os.path.exists(cp):
            return cp
    return None

def analyze_scene(image_path):
    """
    Analyzes an image and classifies it as 'night', 'night_dark', 'day_sunny', or 'day_cloudy'
    based on grayscale luminance and pixel distribution.
    """
    try:
        with Image.open(image_path) as img:
            img_gray = img.convert('L').resize((200, 200))
            hist = img_gray.histogram()
            total_pixels = sum(hist)
            if total_pixels == 0:
                return 'night', 80.0
                
            mean_luminance = sum(i * count for i, count in enumerate(hist)) / total_pixels
            dark_pixels = sum(hist[:40])
            dark_ratio = dark_pixels / total_pixels
            bright_pixels = sum(hist[200:])
            bright_ratio = bright_pixels / total_pixels
            
            # Night detection: Low mean luminance OR high proportion of dark background/shadows
            if mean_luminance < 115 or dark_ratio > 0.35:
                if mean_luminance < 70 or dark_ratio > 0.5:
                    return 'night_dark', mean_luminance
                return 'night', mean_luminance
            elif bright_ratio > 0.25 or mean_luminance > 165:
                return 'day_sunny', mean_luminance
            else:
                return 'day_cloudy', mean_luminance
    except Exception as e:
        print(f"Warning: Could not analyze image {image_path}: {e}")
        return 'night', 80.0

def parse_date_from_filename(filename, file_path):
    """Extracts plausible timestamp from filename or metadata."""
    base = os.path.basename(filename)
    
    # Pattern 1: YYYYMMDD HHMMSS or YYYYMMDD_HHMMSS
    m = re.search(r'(\d{4})(\d{2})(\d{2})[ _](\d{2})(\d{2})(\d{2})', base)
    if m:
        year, month, day, hour, minute, second = m.groups()
        return f"{year}:{month}:{day} {hour}:{minute}:{second}"
        
    # Pattern 2: YYYYMMDD
    m2 = re.search(r'(\d{4})(\d{2})(\d{2})', base)
    if m2:
        year, month, day = m2.groups()
        return f"{year}:{month}:{day} 22:00:00"
        
    # Fallback to file mtime
    try:
        mtime = os.path.getmtime(file_path)
        dt = datetime.fromtimestamp(mtime)
        return dt.strftime("%Y:%m:%d %H:%M:%S")
    except Exception:
        return "2026:08:08 22:30:00"

def get_exif_parameters(scene_type, model="HERO12 Black"):
    """Returns realistic GoPro parameters based on scene type."""
    params = {
        "Make": "GoPro",
        "Model": model,
        "FocalLength": "2.7 mm",
        "FocalLengthIn35mmFormat": "15 mm",
        "FNumber": "2.5",
        "ApertureValue": "2.5",
        "MaxApertureValue": "2.5",
        "ExposureProgram": "Program AE",
        "MeteringMode": "Center-weighted average",
        "Flash": "Off, Did not fire",
        "WhiteBalance": "Auto",
        "ColorSpace": "sRGB",
        "SensingMethod": "One-chip color area sensor",
        "Software": "GoPro Firmware v2.20",
        "CustomRendered": "Normal",
        "ExposureMode": "Auto",
        "DigitalZoomRatio": "1",
        "Contrast": "Normal",
        "Saturation": "Normal",
        "Sharpness": "Hard",
    }
    
    if scene_type == 'night_dark':
        params["ISO"] = "3200"
        params["ExposureTime"] = "1/30"
        params["GainControl"] = "High gain up"
        params["SceneCaptureType"] = "Night"
    elif scene_type == 'night':
        params["ISO"] = "1600"
        params["ExposureTime"] = "1/50"
        params["GainControl"] = "High gain up"
        params["SceneCaptureType"] = "Night"
    elif scene_type == 'day_sunny':
        params["ISO"] = "100"
        params["ExposureTime"] = "1/1000"
        params["GainControl"] = "None"
        params["SceneCaptureType"] = "Standard"
    elif scene_type == 'day_cloudy':
        params["ISO"] = "250"
        params["ExposureTime"] = "1/250"
        params["GainControl"] = "Low gain up"
        params["SceneCaptureType"] = "Standard"
    else:
        params["ISO"] = "100"
        params["ExposureTime"] = "1/500"
        params["GainControl"] = "None"
        params["SceneCaptureType"] = "Standard"
        
    return params

def apply_nik_color_efex_ai_gen_2(
    img, 
    glow_strength=0.25, 
    smear_strength=0.0,
    color_boost=1.25,
    vignette_strength=1.0, 
    grain_strength=1.0,
    use_center_vignette=False
):
    """
    Applies the DxO Nik 7 Color Efex 'AI-gen-2' filter pipeline matching the exact parameters:
    1. Monday Morning: Verschmieren = 0 (keine Unschärfe/Diffusion), Farbe erhöht (+25% Farbsättigung), sanfter Tonalitätslift.
    2. Darken / Lighten Center (optional, default: disabled): Center +25% exposure boost, border -45% vignette falloff.
    3. Dual-Layer Film Grain (450/500 strength): Soft organic grain + crisp high-frequency micro-grain.
    """
    w, h = img.size
    
    # 1. Monday Morning filter (Verschmieren = 0, Farbe/Sättigung erhöht)
    if smear_strength > 0:
        blur_rad = max(1, int(min(w, h) * 0.012 * smear_strength))
        blurred_glow = img.filter(ImageFilter.GaussianBlur(radius=blur_rad))
        glow_enhancer = ImageEnhance.Brightness(blurred_glow)
        bright_glow = glow_enhancer.enhance(1.30)
        img_glow = Image.blend(img, bright_glow, alpha=0.25 * smear_strength)
    else:
        # Verschmieren auf 0: Keine Weichzeichnung / Detailverlust, nur feiner Helligkeitslift
        bright_enhancer = ImageEnhance.Brightness(img)
        img_glow = bright_enhancer.enhance(1.0 + 0.06 * glow_strength)
        
    # Farbe / Farbsättigung erhöhen
    if color_boost > 1.0:
        color_enhancer = ImageEnhance.Color(img_glow)
        img_glow = color_enhancer.enhance(color_boost)
    
    # 2. Darken / Lighten Center (optional, default off; Border: -0.45 = -45%, Center: +0.25 = +25%, CenterSize: 0.55)
    arr = np.array(img_glow, dtype=np.float32)
    if use_center_vignette and vignette_strength > 0:
        y_coords, x_coords = np.mgrid[0:h, 0:w]
        cx, cy = w / 2.0, h / 2.0
        r_norm = np.sqrt(((x_coords - cx) / (w / 2.0))**2 + ((y_coords - cy) / (h / 2.0))**2)
        
        center_size = 0.55
        vignette_t = np.clip((r_norm - center_size) / (1.35 - center_size), 0.0, 1.0)
        vignette_curve = 3.0 * (vignette_t ** 2) - 2.0 * (vignette_t ** 3)
        
        # Center gain +25%, Border darkening -45% (scaled by vignette_strength)
        center_boost = 0.25 * vignette_strength
        border_darken = 0.45 * vignette_strength
        vignette_gain = (1.0 + center_boost * (1.0 - vignette_curve)) * (1.0 - border_darken * vignette_curve)
        arr_vignetted = arr * vignette_gain[:, :, np.newaxis]
    else:
        arr_vignetted = arr
    
    # 3. Dual-Layer Film Grain (Nik strength: 450/500)
    soft_noise = np.random.normal(0, 10.0 * grain_strength, (h, w, 1)).astype(np.float32)
    sharp_noise = np.random.normal(0, 8.0 * grain_strength, (h, w, 1)).astype(np.float32)
    chroma_noise = np.random.normal(0, 3.0 * grain_strength, (h, w, 3)).astype(np.float32)
    
    lum = np.clip((0.299 * arr_vignetted[:, :, 0] + 0.587 * arr_vignetted[:, :, 1] + 0.114 * arr_vignetted[:, :, 2]) / 255.0, 0.0, 1.0)
    sin_lum = np.clip(np.sin(lum * np.pi), 0.0, 1.0)
    grain_mask = np.clip(sin_lum ** 0.7, 0.3, 1.0)
    
    total_grain = (soft_noise + sharp_noise + chroma_noise) * grain_mask[:, :, np.newaxis]
    
    arr_final = np.nan_to_num(arr_vignetted + total_grain, nan=0.0)
    arr_final = np.clip(np.round(arr_final), 0, 255).astype(np.uint8)
    return Image.fromarray(arr_final)

def apply_silver_efex_fine_art(
    img,
    global_contrast=18.58,   # +18.58% in Silver Efex
    soft_contrast=-31.71,    # -31.71% in Silver Efex
    fine_structure=44.51,    # +44.51% fine micro-details
    med_structure=-17.07,    # -17.07% smooth midtones
    grain_strength=1.0       # Grain strength 500
):
    """
    Simulates DxO Silver Efex Pro '019 - Fine Art Process' (019-Fine-art-Prozess):
    - Neutral B&W conversion
    - Global Contrast (+18.6%) & Soft Contrast (-31.7%) for rich blacks and smooth tonal transitions
    - Multi-scale structure: High Fine Structure (+44.5%) + Soft Med Structure (-17.1%)
    - Classic 500-strength Silver Halide Film Grain
    """
    img_gray = img.convert('L')
    w, h = img_gray.size
    arr = np.array(img_gray, dtype=np.float32)

    # 1. Multi-scale Structure Adjustment (Fine Structure +44.5% & Med Structure -17.1%)
    fine_blur = np.array(img_gray.filter(ImageFilter.GaussianBlur(radius=1.2)), dtype=np.float32)
    fine_detail = arr - fine_blur
    
    med_blur = np.array(img_gray.filter(ImageFilter.GaussianBlur(radius=8.0)), dtype=np.float32)
    med_detail = fine_blur - med_blur

    arr_structured = arr + (fine_structure / 100.0) * fine_detail * 1.5 + (med_structure / 100.0) * med_detail * 0.8
    arr_structured = np.clip(arr_structured, 0.0, 255.0)

    # 2. Global Contrast (+18.58%) & Soft Contrast (-31.71%)
    u = arr_structured / 255.0
    s_curve = 3.0 * (u ** 2) - 2.0 * (u ** 3)
    contrast_factor = global_contrast / 100.0
    soft_factor = abs(soft_contrast) / 100.0
    
    u_contrast = (1.0 - contrast_factor) * u + contrast_factor * s_curve
    u_soft = 0.02 + 0.96 * u_contrast
    u_final = (1.0 - 0.3 * soft_factor) * u_contrast + (0.3 * soft_factor) * u_soft
    arr_toned = np.clip(u_final * 255.0, 0.0, 255.0)

    # 3. Silver Halide Film Grain (Silver Efex 500 strength)
    if grain_strength > 0:
        lum_norm = np.clip(arr_toned / 255.0, 0.0, 1.0)
        grain_mask = np.clip(np.sin(lum_norm * np.pi) ** 0.65, 0.25, 1.0)
        
        grain_soft = np.random.normal(0, 7.5 * grain_strength, (h, w)).astype(np.float32)
        grain_sharp = np.random.normal(0, 6.0 * grain_strength, (h, w)).astype(np.float32)
        total_grain = (grain_soft + grain_sharp) * grain_mask
        
        arr_final = np.clip(np.round(arr_toned + total_grain), 0, 255).astype(np.uint8)
    else:
        arr_final = np.clip(np.round(arr_toned), 0, 255).astype(np.uint8)

    img_bw = Image.fromarray(arr_final).convert('RGB')
    return img_bw

def apply_optical_sensor_simulation(
    img, 
    scene_type='night',
    ca_amount=0.0016, 
    base_noise=0.02, 
    black_lift=4.0, 
    highlight_rolloff=252.0, 
    s_strength=0.25,
    diffraction_blur=0.0,
    use_nik_preset=True,
    use_center_vignette=False,
    vignette_strength=1.0,
    smear_strength=0.0,
    color_boost=1.25
):
    """
    Simulates physical camera sensor & lens characteristics + Nik Color Efex processing:
    1. Lateral Chromatic Aberration (TCA): red/blue radial fringing increasing towards edges.
    2. Sensor Tone Curve: S-curve, raised black levels (no 0-clipping), smooth highlight roll-off.
    3. DxO Nik 7 Color Efex 'AI-gen-2' (Monday Morning: Verschmieren=0, Farbe erhöht; Film grain).
    4. CMOS Sensor Noise: Gaussian monochrome & subtle chroma noise, higher in shadows.
    """
    w, h = img.size
    
    # 1. Subtle optical diffraction softening (if enabled)
    if diffraction_blur > 0:
        blurred = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        img = Image.blend(img, blurred, alpha=diffraction_blur)
        
    # 2. Transverse Chromatic Aberration (Radial TCA)
    if ca_amount > 0:
        cx, cy = w / 2.0, h / 2.0
        r, g, b = img.split()
        
        # Red expands radially outward
        sr = 1.0 + ca_amount
        matrix_r = (1.0 / sr, 0, cx * (1.0 - 1.0 / sr), 0, 1.0 / sr, cy * (1.0 - 1.0 / sr))
        r_warped = r.transform((w, h), Image.Transform.AFFINE, matrix_r, Image.Resampling.BICUBIC)
        
        # Blue contracts radially inward
        sb = 1.0 - ca_amount
        matrix_b = (1.0 / sb, 0, cx * (1.0 - 1.0 / sb), 0, 1.0 / sb, cy * (1.0 - 1.0 / sb))
        b_warped = b.transform((w, h), Image.Transform.AFFINE, matrix_b, Image.Resampling.BICUBIC)
        
        img = Image.merge('RGB', (r_warped, g, b_warped))
        
    # 3. Sensor Tone Curve & S-Curve
    arr = np.array(img, dtype=np.float32)
    u = arr / 255.0
    s_curve = 3.0 * (u ** 2) - 2.0 * (u ** 3)
    blended = (1.0 - s_strength) * u + s_strength * s_curve
    tone_mapped = black_lift + blended * (highlight_rolloff - black_lift)
    tone_mapped = np.clip(np.round(tone_mapped), 0, 255).astype(np.uint8)
    img_toned = Image.fromarray(tone_mapped)
    
    # 4. DxO Nik 7 Color Efex 'AI-gen-2' processing
    if use_nik_preset:
        img_toned = apply_nik_color_efex_ai_gen_2(
            img_toned,
            smear_strength=smear_strength,
            color_boost=color_boost,
            use_center_vignette=use_center_vignette,
            vignette_strength=vignette_strength
        )
    
    # 5. CMOS Sensor Noise Injection
    arr_toned = np.array(img_toned, dtype=np.float32)
    u_toned = arr_toned / 255.0
    
    if 'night' in scene_type:
        noise_factor = base_noise * (1.1 if scene_type == 'night_dark' else 0.9)
    else:
        noise_factor = base_noise * 0.55
        
    if noise_factor > 0:
        lum = 0.299 * u_toned[:, :, 0] + 0.587 * u_toned[:, :, 1] + 0.114 * u_toned[:, :, 2]
        shadow_weight = 0.8 + 0.3 * (1.0 - np.clip(lum, 0.0, 1.0))
        sigma = 255.0 * noise_factor * shadow_weight[:, :, np.newaxis]
        
        mono_noise = np.random.normal(0, 1.0, (h, w, 1)).astype(np.float32)
        color_noise = np.random.normal(0, 1.0, (h, w, 3)).astype(np.float32)
        total_noise = (0.85 * mono_noise + 0.15 * color_noise) * sigma
        
        final_arr = arr_toned + total_noise
    else:
        final_arr = arr_toned
        
    final_arr = np.clip(np.round(final_arr), 0, 255).astype(np.uint8)
    return Image.fromarray(final_arr)

def inject_exif_with_exiftool(exiftool_bin, image_path, params, timestamp, backup=False):
    """Executes exiftool to inject GoPro metadata."""
    cmd = [exiftool_bin]
    
    if not backup:
        cmd.append("-overwrite_original")
        
    for k, v in params.items():
        cmd.append(f"-{k}={v}")
        
    if timestamp:
        cmd.append(f"-DateTimeOriginal={timestamp}")
        cmd.append(f"-CreateDate={timestamp}")
        cmd.append(f"-ModifyDate={timestamp}")
        
    cmd.append(image_path)
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"ExifTool failed: {res.stderr or res.stdout}")
    return res.stdout

def inject_exif_with_piexif(image_path, params, timestamp):
    """Fallback Python-only injection using piexif."""
    import piexif
    from fractions import Fraction

    zeroth_ifd = {
        piexif.ImageIFD.Make: params["Make"].encode('utf-8'),
        piexif.ImageIFD.Model: params["Model"].encode('utf-8'),
        piexif.ImageIFD.Software: params["Software"].encode('utf-8'),
    }
    
    if timestamp:
        zeroth_ifd[piexif.ImageIFD.DateTime] = timestamp.encode('utf-8')
        
    exp_frac = Fraction(params["ExposureTime"])
    
    exif_ifd = {
        piexif.ExifIFD.FocalLength: (27, 10),
        piexif.ExifIFD.FocalLengthIn35mmFilm: int(params["FocalLengthIn35mmFormat"].replace(" mm", "")),
        piexif.ExifIFD.FNumber: (25, 10),
        piexif.ExifIFD.ISOSpeedRatings: int(params["ISO"]),
        piexif.ExifIFD.ExposureTime: (exp_frac.numerator, exp_frac.denominator),
        piexif.ExifIFD.ExposureProgram: 2,
        piexif.ExifIFD.MeteringMode: 2,
        piexif.ExifIFD.Flash: 0,
        piexif.ExifIFD.WhiteBalance: 0,
        piexif.ExifIFD.ColorSpace: 1,
        piexif.ExifIFD.SensingMethod: 2,
        piexif.ExifIFD.CustomRendered: 0,
        piexif.ExifIFD.ExposureMode: 0,
        piexif.ExifIFD.SceneCaptureType: 3 if "Night" in params["SceneCaptureType"] else 0,
    }
    
    if timestamp:
        exif_ifd[piexif.ExifIFD.DateTimeOriginal] = timestamp.encode('utf-8')
        exif_ifd[piexif.ExifIFD.DateTimeDigitized] = timestamp.encode('utf-8')
        
    exif_dict = {"0th": zeroth_ifd, "Exif": exif_ifd}
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)

def get_versioned_filename(file_path, suffix=""):
    """Generates a new filepath with an incremented version number (_v1, _v2, etc.) and optional suffix."""
    dirname, basename = os.path.split(file_path)
    name, ext = os.path.splitext(basename)
    
    m = re.match(r'^(.*?)(?:_v(\d+))$', name)
    if m:
        base_root = m.group(1)
        current_v = int(m.group(2))
        start_v = current_v + 1
    else:
        base_root = name
        start_v = 1
        
    v = start_v
    while True:
        candidate_name = f"{base_root}_v{v}{suffix}{ext}"
        candidate_path = os.path.join(dirname, candidate_name)
        if not os.path.exists(candidate_path):
            return candidate_path
        v += 1

def filter_input_files(file_paths):
    """
    When processing a batch of files in a directory, avoids redundant processing
    of generated _v<N> files if the unversioned base file exists in the directory.
    """
    basenames = {os.path.basename(p): p for p in file_paths}
    selected = []
    for p in file_paths:
        base = os.path.basename(p)
        name, ext = os.path.splitext(base)
        m = re.match(r'^(.*?)(?:_v\d+.*)$', name)
        if m:
            base_original = f"{m.group(1)}{ext}"
            if base_original in basenames:
                continue
        selected.append(p)
    return selected

def process_file(
    image_path, 
    exiftool_bin, 
    scene_override=None, 
    model="HERO12 Black", 
    apply_effects=True,
    use_nik_preset=True,
    use_center_vignette=False,
    vignette_strength=1.0,
    smear_strength=0.0,
    color_boost=1.25,
    ca_amount=0.0016,
    noise_amount=0.018,
    black_lift=4.0,
    backup=False,
    jpeg_quality=97,
    versioned=True,
    create_bw=False,
    bw_only=False,
    bw_suffix="_NIK"
):
    """
    Processes an image file with optical simulation, Nik Color Efex filter,
    optional DxO Silver Efex '019 - Fine Art Process' B&W version, and EXIF injection.
    """
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found.")
        return []
        
    target_path = get_versioned_filename(image_path) if versioned else image_path
    
    if scene_override:
        scene = scene_override
        lum = 0.0
    else:
        scene, lum = analyze_scene(image_path)
        
    params = get_exif_parameters(scene, model=model)
    timestamp = parse_date_from_filename(image_path, image_path)
    
    in_name = os.path.basename(image_path)
    out_name = os.path.basename(target_path)
    target_info = f" -> {out_name}" if versioned else ""
    print(f"-> Processing: {in_name}{target_info}")
    print(f"   Scene: {scene} (Mean Lum: {lum:.1f})")
    print(f"   Camera: {params['Make']} {params['Model']}")
    print(f"   Lens: {params['FocalLength']} (35mm: {params['FocalLengthIn35mmFormat']}), f/{params['FNumber']}")
    print(f"   Exposure: ISO {params['ISO']}, {params['ExposureTime']}s, {params['ExposureProgram']}")
    print(f"   Timestamp: {timestamp}")
    
    generated_files = []
    
    try:
        # Step 1: Process Color Version (unless bw_only is requested)
        if not bw_only:
            if apply_effects:
                if use_nik_preset:
                    vignette_desc = " (+ Center-Vignette)" if (use_center_vignette and vignette_strength > 0) else ""
                    smear_desc = f", Verschmieren: {smear_strength}" if smear_strength > 0 else ""
                    color_desc = f", Farbe: +{int((color_boost-1.0)*100)}%" if color_boost != 1.0 else ""
                    nik_info = f" + Nik 7 Color Efex 'Ai-gen-2'{vignette_desc}{color_desc}{smear_desc}"
                else:
                    nik_info = ""
                print(f"   Applying Color & Sensor Simulation (CA: {ca_amount:.4f}, Noise: {noise_amount*100:.1f}%, S-Curve{nik_info})...")
                with Image.open(image_path) as img:
                    img_rgb = img.convert('RGB')
                    processed_img = apply_optical_sensor_simulation(
                        img_rgb,
                        scene_type=scene,
                        ca_amount=ca_amount,
                        base_noise=noise_amount,
                        black_lift=black_lift,
                        use_nik_preset=use_nik_preset,
                        use_center_vignette=use_center_vignette,
                        vignette_strength=vignette_strength,
                        smear_strength=smear_strength,
                        color_boost=color_boost
                    )
                    processed_img.save(target_path, quality=jpeg_quality, subsampling=0)
            elif versioned:
                import shutil
                shutil.copy2(image_path, target_path)
                    
            # EXIF Metadata Injection for Color Image
            if exiftool_bin:
                inject_exif_with_exiftool(exiftool_bin, target_path, params, timestamp, backup=backup)
            else:
                inject_exif_with_piexif(target_path, params, timestamp)
                
            print(f"   Status: SUCCESS -> Color: {out_name}")
            generated_files.append(target_path)

        # Step 2: Process Additional S/W Fine-Art Version (DxO Silver Efex '019 - Fine Art Process')
        if create_bw or bw_only:
            bw_target_path = get_versioned_filename(image_path, suffix=bw_suffix) if versioned else f"{os.path.splitext(image_path)[0]}{bw_suffix}{os.path.splitext(image_path)[1]}"
            bw_name = os.path.basename(bw_target_path)
            print(f"   Applying DxO Silver Efex Pro '019 - Fine Art Process' (+18.6% Contrast, -31.7% Soft, +44.5% Fine Structure, Silver Halide Grain 500)...")
            
            with Image.open(image_path) as img:
                img_rgb = img.convert('RGB')
                bw_img = apply_silver_efex_fine_art(img_rgb)
                bw_img.save(bw_target_path, quality=jpeg_quality, subsampling=0)
                
            # EXIF Metadata Injection for S/W Image
            if exiftool_bin:
                inject_exif_with_exiftool(exiftool_bin, bw_target_path, params, timestamp, backup=backup)
            else:
                inject_exif_with_piexif(bw_target_path, params, timestamp)
                
            print(f"   Status: SUCCESS -> S/W Fine Art: {bw_name}")
            generated_files.append(bw_target_path)
            
        print()
        return generated_files
    except Exception as e:
        print(f"   Status: FAILED - {e}\n")
        return []

def open_in_nik_color_efex(image_paths):
    """Opens image files in DxO Nik 7 Color Efex standalone app."""
    if not os.path.exists(NIK_EXE_PATH):
        print(f"DxO Nik 7 Color Efex executable not found at: {NIK_EXE_PATH}")
        return
    for p in image_paths:
        print(f"Opening in DxO Nik 7 Color Efex: {p}")
        subprocess.Popen([NIK_EXE_PATH, p])

def main():
    parser = argparse.ArgumentParser(description="Inject realistic GoPro EXIF metadata, optical sensor simulation, DxO Nik 7 Color Efex & DxO Silver Efex '019 - Fine Art Process' with auto-versioning.")
    parser.add_argument("target", help="Target image file or directory.")
    parser.add_argument("--scene", choices=["auto", "night", "night_dark", "day", "day_sunny", "day_cloudy"], default="auto",
                        help="Override automatic scene detection (default: auto).")
    parser.add_argument("--model", choices=["HERO12 Black", "HERO11 Black", "HERO10 Black", "HERO9 Black"], default="HERO12 Black",
                        help="GoPro camera model (default: HERO12 Black).")
    parser.add_argument("--no-effects", action="store_true", help="Skip optical & sensor noise simulation (EXIF only).")
    parser.add_argument("--no-nik", action="store_true", help="Skip Nik 7 Color Efex 'Ai-gen-2' filter processing.")
    parser.add_argument("--smear", type=float, default=0.0,
                        help="Monday Morning Verschmieren/Smear diffusion strength (default: 0.0 = disabled).")
    parser.add_argument("--color", "--color-boost", "--saturation", type=float, default=1.25,
                        help="Monday Morning Farbe/Saturation multiplier (default: 1.25 = +25 percent).")
    parser.add_argument("--center-vignette", "--vignette", action="store_true",
                        help="Enable Darken / Lighten Center (+25 percent center boost & edge vignette falloff). Default: disabled.")
    parser.add_argument("--vignette-strength", type=float, default=1.0,
                        help="Darken / Lighten Center strength multiplier when enabled (default: 1.0).")
    parser.add_argument("--bw", "--silver-efex", "--fine-art", action="store_true",
                        help="Zusätzlich eine S/W-Version mit DxO Silver Efex '019 - Fine Art Process' erstellen.")
    parser.add_argument("--bw-only", action="store_true",
                        help="Nur die S/W Fine Art Version erstellen (ohne Farbbild).")
    parser.add_argument("--bw-suffix", default="_NIK",
                        help="Suffix für die S/W-Version (Standard: '_NIK').")
    parser.add_argument("--no-version", "--overwrite", action="store_true",
                        help="Overwrite existing file in-place instead of creating a new versioned file (_v1, _v2, etc.).")
    parser.add_argument("--open-nik", action="store_true", help="Open processed image(s) in DxO Nik 7 Color Efex GUI.")
    parser.add_argument("--ca", type=float, default=0.0016, help="Chromatic aberration strength (default: 0.0016).")
    parser.add_argument("--noise", type=float, default=0.018, help="Base sensor noise ratio (default: 0.018 = 1.8 percent).")
    parser.add_argument("--black-lift", type=float, default=4.0, help="Black level lift in 8-bit scale (default: 4.0).")
    parser.add_argument("--quality", type=int, default=97, help="JPEG save quality (default: 97).")
    parser.add_argument("--backup", action="store_true", help="Keep original backup file when using ExifTool.")
    
    args = parser.parse_args()
    
    exiftool_bin = find_exiftool()
    if exiftool_bin:
        print(f"Using ExifTool: {exiftool_bin}")
    else:
        print("ExifTool not found. Using piexif fallback.")
        
    scene_override = None if args.scene == "auto" else args.scene
    if scene_override == "day":
        scene_override = "day_sunny"
        
    apply_effects = not args.no_effects
    use_nik = not args.no_nik
    use_center_vignette = args.center_vignette and (args.vignette_strength > 0)
    vignette_strength = args.vignette_strength if use_center_vignette else 0.0
    smear_val = args.smear / 100.0 if args.smear > 1.0 else args.smear
    smear_strength = max(0.0, smear_val)
    if args.color == 0.0:
        color_boost = 1.0
    elif args.color > 1.5:
        color_boost = 1.0 + (args.color / 100.0)
    elif args.color > 0.0 and args.color < 1.0:
        color_boost = 1.0 + args.color
    else:
        color_boost = max(0.0, args.color)
    versioned = not args.no_version
    target = os.path.abspath(args.target)
    
    processed_files = []
    if os.path.isdir(target):
        raw_files = [os.path.join(target, f) for f in os.listdir(target) if f.lower().endswith(('.jpg', '.jpeg'))]
        if not raw_files:
            print(f"No JPEG images found in {target}")
            return
        files = filter_input_files(raw_files)
        print(f"Found {len(files)} image(s) in '{target}'. Processing (Auto-Versioning: {'ON' if versioned else 'OFF'}, B&W Fine Art: {'ON' if (args.bw or args.bw_only) else 'OFF'})...\n")
        for f in files:
            outs = process_file(
                f, 
                exiftool_bin, 
                scene_override, 
                args.model, 
                apply_effects=apply_effects,
                use_nik_preset=use_nik,
                use_center_vignette=use_center_vignette,
                vignette_strength=vignette_strength,
                smear_strength=smear_strength,
                color_boost=color_boost,
                ca_amount=args.ca,
                noise_amount=args.noise,
                black_lift=args.black_lift,
                backup=args.backup,
                jpeg_quality=args.quality,
                versioned=versioned,
                create_bw=args.bw,
                bw_only=args.bw_only,
                bw_suffix=args.bw_suffix
            )
            processed_files.extend(outs)
        print(f"Finished: {len(processed_files)} images created successfully.")
    elif os.path.isfile(target):
        outs = process_file(
            target, 
            exiftool_bin, 
            scene_override, 
            args.model, 
            apply_effects=apply_effects,
            use_nik_preset=use_nik,
            use_center_vignette=use_center_vignette,
            vignette_strength=vignette_strength,
            smear_strength=smear_strength,
            color_boost=color_boost,
            ca_amount=args.ca,
            noise_amount=args.noise,
            black_lift=args.black_lift,
            backup=args.backup,
            jpeg_quality=args.quality,
            versioned=versioned,
            create_bw=args.bw,
            bw_only=args.bw_only,
            bw_suffix=args.bw_suffix
        )
        processed_files.extend(outs)
    else:
        print(f"Target '{args.target}' does not exist.")

    if args.open_nik and processed_files:
        open_in_nik_color_efex(processed_files)

if __name__ == "__main__":
    main()

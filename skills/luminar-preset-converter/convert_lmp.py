#!/usr/bin/env python3
import os
import sys
import re
import json
import uuid
import plistlib
import argparse
import xml.etree.ElementTree as ET

# Parameter-Mapping von Adobe Lightroom (XMP) -> Luminar Neo MIPL
XMP_PARAM_MAP = {
    'Exposure2012': ('MIPLExposureEffect', 'Exposure', lambda x: float(x) * 20.0),
    'Contrast2012': ('MIPLContrastEffect', 'Contrast', lambda x: float(x)),
    'Highlights2012': ('MIPLHighlightsEffect', 'Highlights', lambda x: float(x)),
    'Shadows2012': ('MIPLDynBrightnessEffect', 'Smart Tone', lambda x: float(x)),
    'Whites2012': ('MIPLBlackWhiteEffect', 'Whites', lambda x: float(x)),
    'Blacks2012': ('MIPLBlackWhiteEffect', 'Blacks', lambda x: float(x)),
    'Clarity2012': ('MIPLClarityEffect', 'Clarity', lambda x: float(x)),
    'Vibrance': ('MIPLVibranceEffect', 'Vibrance', lambda x: float(x)),
    'Saturation': ('MIPLSaturationEffect', 'Saturation', lambda x: float(x)),
    'Dehaze': ('MIPLDehazeEffect', 'Dehaze', lambda x: float(x)),
    'Sharpness': ('MIPLSharpenEffect', 'Radius', lambda x: float(x)),
    'Temperature': ('MIPLDevelopCommonEffectID', 'Temperature', lambda x: float(x)),
    'Tint': ('MIPLDevelopCommonEffectID', 'Tint', lambda x: float(x)),
    'PostCropVignetteAmount': ('MIPLVignetteEffect', 'Amount', lambda x: float(x)),
    'GrainAmount': ('MIPLGrainNewEffect', 'Amount', lambda x: float(x)),
}

def convert_mipl_effect(eff):
    """Wandelt einen MIPL-Effekt aus dem Apple Plist XML Format in das Luminar Neo JSON Format um."""
    ident = eff.get('Identifier', '')
    params = eff.get('Parameters', {})
    params_array = []

    if isinstance(params, dict):
        for p_name, p_val in params.items():
            val = p_val.get('Value', 0) if isinstance(p_val, dict) else p_val
            opt_type = p_val.get('OptionalDataType', 0) if isinstance(p_val, dict) else 0
            opt_val = p_val.get('OptionalDataValue', 0) if isinstance(p_val, dict) else 0
            params_array.append({
                'name': str(p_name),
                'value': str(val),
                'default': '0',
                'min': '-100',
                'max': '100',
                'opt_data_type': str(opt_type),
                'opt_data_value': str(opt_val)
            })

    return {
        'id': str(ident),
        'params_array': params_array
    }

def parse_xmp_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    params = {}
    try:
        root = ET.fromstring(content)
        for elem in root.iter():
            for k, v in elem.attrib.items():
                clean_k = k.split('}')[-1]
                if clean_k.startswith('crs:'):
                    clean_k = clean_k[4:]
                params[clean_k] = v
    except Exception:
        pass

    matches = re.findall(r'crs:([A-Za-z0-9_]+)\s*=\s*"([^"]+)"', content)
    for k, v in matches:
        params[k] = v

    matches_elem = re.findall(r'<crs:([A-Za-z0-9_]+)>([^<]+)</crs:([A-Za-z0-9_]+)>', content)
    for k1, v, k2 in matches_elem:
        if k1 == k2:
            params[k1] = v

    # Fallback für alte .lrtemplate Textdateien (key = value)
    matches_lrtemplate = re.findall(r'([A-Za-z0-9_]+)\s*=\s*([+\-0-9.]+)', content)
    for k, v in matches_lrtemplate:
        if k not in params:
            params[k] = v

    return params

def convert_xmp_file(p_path, preset_name=None):
    params = parse_xmp_file(p_path)
    if not preset_name:
        preset_name = params.get('PresetName', os.path.splitext(os.path.basename(p_path))[0])

    effects_by_id = {}
    for xmp_key, (effect_id, param_name, transform_fn) in XMP_PARAM_MAP.items():
        if xmp_key in params:
            val_str = params[xmp_key]
            try:
                trans_val = transform_fn(val_str)
            except Exception:
                trans_val = val_str

            if effect_id not in effects_by_id:
                effects_by_id[effect_id] = []

            effects_by_id[effect_id].append({
                'name': param_name,
                'value': str(trans_val),
                'default': '0',
                'min': '-100',
                'max': '100',
                'opt_data_type': '0',
                'opt_data_value': '0'
            })

    effects_array = []
    for eff_id, params_arr in effects_by_id.items():
        effects_array.append({
            'id': eff_id,
            'params_array': params_arr
        })

    return create_template_json(preset_name, effects_array)

def convert_lmp_file(p_path, preset_name=None):
    """Liest ein XML .lmp Plist File und gibt ein Luminar Neo JSON-Template Dict zurück."""
    if not preset_name:
        preset_name = os.path.splitext(os.path.basename(p_path))[0]

    with open(p_path, 'rb') as fp:
        plist_data = plistlib.load(fp)

    effects_array = []
    for layer in plist_data.get('AdjustmentLayers', []):
        for eff in layer.get('Effects', []):
            effects_array.append(convert_mipl_effect(eff))

    return create_template_json(preset_name, effects_array)

def create_template_json(preset_name, effects_array):
    preset_uuid = str(uuid.uuid4())
    template_json = {
        'name': preset_name,
        'uuid': preset_uuid,
        'creation_info': {
            'app_name': 'LUMINAR_NEO',
            'mipl_version': '2.1.24.0',
            'platform': 'Win',
            'resource_version': '0.1',
            'preset_version': '0.2'
        },
        'layers_array': [
            {
                'layer_name': '',
                'layer_type': '0',
                'enabled': 'true',
                'alive': 'true',
                'curr_edit_inedx': '0',
                'source_image': '',
                'mask': '',
                'mask_setting': {'density': '0', 'feather': '0', 'expand': '0'},
                'mask_type': '0',
                'scale_mode': '0',
                'blend_mode': '0',
                'opacity': '1',
                'default_blend_mode': '0',
                'default_opacity': '1',
                'base_image_modified_data': '',
                'base_image_modified_alpha': '',
                'layer_generative_type': '0',
                'transformation': ['1', '0', '0', '1', '0', '0'],
                'edits_array': [
                    {
                        'id': '13335248785024620168-1990478318568052589-3407127120591755155-5438302987486979857',
                        'edit_name': '',
                        'permanent': 'false',
                        'locked': 'false',
                        'enabled': 'true',
                        'tool_name': 'DefaultEffects',
                        'mask_setting': {'density': '0', 'feather': '0', 'expand': '0'},
                        'mask': '',
                        'source_image': '',
                        'blend_mode': '0',
                        'effects_array': effects_array
                    }
                ]
            }
        ],
        'canvas_size': {'w': '2560', 'h': '1600'}
    }
    return template_json, len(effects_array)

def process_preset_files(preset_filepaths, output_dir):
    """Konvertiert eine Liste von .lmp / .xmp / .lrtemplate Dateien nach Presets/Users."""
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n--- Konvertiere {len(preset_filepaths)} Preset-Datei(en) nach '{output_dir}' ---")

    converted_count = 0
    for p_path in sorted(preset_filepaths):
        f_name = os.path.basename(p_path)
        ext = os.path.splitext(f_name)[1].lower()
        preset_name = os.path.splitext(f_name)[0]

        try:
            if ext == '.lmp':
                template_json, count = convert_lmp_file(p_path, preset_name)
            elif ext in ('.xmp', '.lrtemplate'):
                template_json, count = convert_xmp_file(p_path, preset_name)
            else:
                continue

            lnp_dir = os.path.join(output_dir, f"{preset_name}.lnp")
            os.makedirs(lnp_dir, exist_ok=True)

            lmps_file = os.path.join(lnp_dir, 'template.lmps')
            with open(lmps_file, 'w', encoding='utf-8') as out_f:
                json.dump(template_json, out_f, indent=4)

            converted_count += 1
            print(f" [OK] '{preset_name}.lnp/template.lmps' ({count} Effekte aus {ext})")
        except Exception as e:
            print(f" [ERROR] Konnte '{f_name}' nicht konvertieren: {e}")

    print(f"\nErfolgreich {converted_count} Presets für Luminar Neo konvertiert!")

def search_and_convert(root_dir, output_dir=None):
    root_dir = os.path.abspath(root_dir)
    print(f"Durchsuche Verzeichnis '{root_dir}' nach .lmp, .xmp und .lrtemplate Dateien...")

    preset_files = []
    for r, d, files in os.walk(root_dir):
        for f in files:
            if f.lower().endswith(('.lmp', '.xmp', '.lrtemplate')):
                full_p = os.path.join(r, f)
                preset_files.append(full_p)

    if not preset_files:
        print(f"Keine .lmp, .xmp oder .lrtemplate Dateien in '{root_dir}' gefunden.")
        return

    default_neo_users = os.path.expanduser(r'~\AppData\Roaming\Luminar Neo\Data\Presets\Users')
    target_out = output_dir if output_dir else default_neo_users
    if not os.path.exists(target_out):
        target_out = root_dir

    process_preset_files(preset_files, target_out)

def main():
    parser = argparse.ArgumentParser(description="Konvertiert alte Luminar *.lmp sowie Adobe Lightroom *.xmp/*.lrtemplate Presets in das native Luminar Neo Format (.lnp/template.lmps).")
    parser.add_argument("src_dir", nargs="?", default=".", help="Pfad zum Quellordner oder Projektverzeichnis (Standard: aktuelles Verzeichnis)")
    parser.add_argument("--out", help="Zielverzeichnis für konvertierte .lnp Presets", default=None)

    args = parser.parse_args()
    search_and_convert(args.src_dir, args.out)

if __name__ == '__main__':
    main()

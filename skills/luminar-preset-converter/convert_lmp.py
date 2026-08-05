#!/usr/bin/env python3
import os
import sys
import json
import uuid
import plistlib
import argparse

def convert_effect(eff):
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

def convert_lmp_file(p_path, preset_name=None):
    """Liest ein XML .lmp Plist File und gibt ein Luminar Neo JSON-Template Dict zurück."""
    if not preset_name:
        preset_name = os.path.splitext(os.path.basename(p_path))[0]

    with open(p_path, 'rb') as fp:
        plist_data = plistlib.load(fp)

    effects_array = []
    for layer in plist_data.get('AdjustmentLayers', []):
        for eff in layer.get('Effects', []):
            effects_array.append(convert_effect(eff))

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

def process_lmp_files(lmp_filepaths, output_dir):
    """Konvertiert eine Liste von .lmp-Dateien direkt in den Root-Ordner Presets/Users von Luminar Neo."""
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n--- Konvertiere {len(lmp_filepaths)} .lmp Datei(en) direkt nach '{output_dir}' ---")

    converted_count = 0
    for p_path in sorted(lmp_filepaths):
        f_name = os.path.basename(p_path)
        preset_name = os.path.splitext(f_name)[0]
        try:
            template_json, count = convert_lmp_file(p_path, preset_name)
            
            # Erstelle nativer .lnp Ordner direkt im Root-Ordner Presets/Users
            lnp_dir = os.path.join(output_dir, f"{preset_name}.lnp")
            os.makedirs(lnp_dir, exist_ok=True)
            
            # Schreibe template.lmps im unkomprimierten JSON Format
            lmps_file = os.path.join(lnp_dir, 'template.lmps')
            with open(lmps_file, 'w', encoding='utf-8') as out_f:
                json.dump(template_json, out_f, indent=4)

            converted_count += 1
            print(f" [OK] '{preset_name}.lnp/template.lmps' ({count} Effekte)")
        except Exception as e:
            print(f" [ERROR] Konnte '{f_name}' nicht konvertieren: {e}")

    print(f"\nErfolgreich {converted_count} Presets direkt im Root-Ordner von Luminar Neo erstellt!")

def search_and_convert(root_dir, output_dir=None):
    root_dir = os.path.abspath(root_dir)
    print(f"Durchsuche Verzeichnis '{root_dir}' nach .lmp Dateien...")

    lmp_files = []
    for r, d, files in os.walk(root_dir):
        for f in files:
            if f.lower().endswith('.lmp'):
                full_p = os.path.join(r, f)
                lmp_files.append(full_p)

    if not lmp_files:
        print(f"Keine .lmp Dateien in '{root_dir}' gefunden.")
        return

    # Standardausgabe ist immer direkt das Luminar Neo User Preset Verzeichnis
    default_neo_users = os.path.expanduser(r'~\AppData\Roaming\Luminar Neo\Data\Presets\Users')
    target_out = output_dir if output_dir else default_neo_users
    if not os.path.exists(target_out):
        target_out = root_dir

    process_lmp_files(lmp_files, target_out)

def main():
    parser = argparse.ArgumentParser(description="Konvertiert alte Luminar *.lmp Presets direkt in den Root-Ordner von Luminar Neo (.lnp/template.lmps).")
    parser.add_argument("src_dir", nargs="?", default=".", help="Pfad zum Quellordner oder Projektverzeichnis (Standard: aktuelles Verzeichnis)")
    parser.add_argument("--out", help="Zielverzeichnis für konvertierte .lnp Presets", default=None)

    args = parser.parse_args()
    search_and_convert(args.src_dir, args.out)

if __name__ == '__main__':
    main()

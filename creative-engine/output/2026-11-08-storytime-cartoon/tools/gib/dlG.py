"""Haal keyframes op: python3 dlG.py N05=<job-url-deel> ...  (deel = hf_<datum>_<tijd>_<job>.png); de vorige versie gaat naar kfG/old/."""
import sys, os, shutil, subprocess
B = 'https://d8j0ntlcm91z4.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/'
os.makedirs('kfG/old', exist_ok=True)
for a in sys.argv[1:]:
    k, part = a.split('=', 1); dst = f'kfG/{k}.png'
    if os.path.exists(dst):
        n = 1
        while os.path.exists(f'kfG/old/{k}_v{n}.png'): n += 1
        shutil.move(dst, f'kfG/old/{k}_v{n}.png')
    subprocess.run(['curl', '-sS', '-o', dst, B + part], check=True); print(k, os.path.getsize(dst))

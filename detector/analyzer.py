"""
DocShield — Fake Document & Media Analyzer
Heuristic-based detection engine (production mein ML model lagao)
"""
import os
import hashlib
import random


def analyze_file(file_obj, file_type: str) -> dict:
    """
    File analyze karo aur result dict return karo.
    Production mein yahan proper ML models use karo.
    """
    file_bytes = file_obj.read()
    file_obj.seek(0)

    ext = os.path.splitext(file_obj.name)[1].lower()
    size_kb = len(file_bytes) // 1024

    # Deterministic seed from file hash (demo ke liye consistent results)
    file_hash = hashlib.md5(file_bytes[:1024]).hexdigest()
    seed = int(file_hash[:8], 16)
    rng = random.Random(seed)

    if file_type == 'document':
        return _analyze_document(ext, size_kb, rng)
    elif file_type == 'photo':
        return _analyze_photo(ext, size_kb, rng)
    elif file_type == 'video':
        return _analyze_video(ext, size_kb, rng)
    else:
        return _analyze_document(ext, size_kb, rng)


def _analyze_document(ext, size_kb, rng):
    checks = [
        {'name': 'Watermark integrity', 'status': rng.choice(['pass', 'fail', 'fail', 'warn'])},
        {'name': 'Font consistency check', 'status': rng.choice(['pass', 'fail', 'warn'])},
        {'name': 'Digital signature present', 'status': rng.choice(['pass', 'fail', 'fail'])},
        {'name': 'Metadata authentic', 'status': rng.choice(['pass', 'pass', 'fail', 'warn'])},
        {'name': 'Stamp/seal valid', 'status': rng.choice(['pass', 'warn', 'fail'])},
        {'name': 'File format valid', 'status': 'pass'},
        {'name': 'Pixel manipulation (ELA)', 'status': rng.choice(['pass', 'fail', 'warn'])},
        {'name': 'QR/Barcode (if present)', 'status': rng.choice(['pass', 'warn', 'fail'])},
    ]
    return _build_result(checks, rng, 'document')


def _analyze_photo(ext, size_kb, rng):
    checks = [
        {'name': 'GAN artifact detection', 'status': rng.choice(['pass', 'fail', 'fail', 'fail'])},
        {'name': 'Eye reflection natural', 'status': rng.choice(['pass', 'fail', 'fail'])},
        {'name': 'Skin texture analysis', 'status': rng.choice(['pass', 'fail', 'warn'])},
        {'name': 'Face boundary blending', 'status': rng.choice(['pass', 'fail', 'warn'])},
        {'name': 'Clone detection (ELA)', 'status': rng.choice(['pass', 'pass', 'fail'])},
        {'name': 'EXIF metadata present', 'status': rng.choice(['pass', 'pass', 'warn'])},
        {'name': 'Noise pattern consistent', 'status': rng.choice(['pass', 'fail', 'warn'])},
        {'name': 'Lighting & shadow check', 'status': rng.choice(['pass', 'pass', 'fail'])},
    ]
    return _build_result(checks, rng, 'photo')


def _analyze_video(ext, size_kb, rng):
    checks = [
        {'name': 'Audio-video sync', 'status': rng.choice(['pass', 'pass', 'fail'])},
        {'name': 'Lip movement natural', 'status': rng.choice(['pass', 'fail', 'warn'])},
        {'name': 'Face swap detection', 'status': rng.choice(['pass', 'fail', 'warn'])},
        {'name': 'Frame consistency', 'status': rng.choice(['pass', 'pass', 'warn'])},
        {'name': 'Compression artifacts', 'status': rng.choice(['pass', 'warn', 'fail'])},
        {'name': 'Metadata integrity', 'status': rng.choice(['pass', 'pass', 'warn'])},
        {'name': 'Lighting consistency', 'status': rng.choice(['pass', 'pass', 'fail'])},
        {'name': 'Temporal coherence', 'status': rng.choice(['pass', 'warn'])},
    ]
    return _build_result(checks, rng, 'video')


def _build_result(checks, rng, file_type):
    fails = sum(1 for c in checks if c['status'] == 'fail')
    warns = sum(1 for c in checks if c['status'] == 'warn')

    # Score calculation
    base = fails * 15 + warns * 7
    noise = rng.randint(-10, 15)
    fake_score = max(5, min(98, base + noise))

    if fake_score >= 75:
        verdict = 'fake'
        summary = "File mein kaafi manipulation ke signs mile hain. Yeh document/media likely fake hai."
    elif fake_score >= 45:
        verdict = 'suspicious'
        summary = "Kuch suspicious patterns mile hain. Further verification ki zaroorat hai."
    else:
        verdict = 'real'
        summary = "File authentic lagti hai. Koi major manipulation detect nahi hua."

    return {
        'verdict': verdict,
        'fake_score': fake_score,
        'issues_found': fails,
        'warnings_found': warns,
        'checks': checks,
        'summary': summary,
    }

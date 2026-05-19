import ssl
import requests
import hashlib
import time
import random
import string
import hmac

SERVER_URL = "https://ipsniper.kesug.com/sniper/api.php?action=activate"
EXPECTED_PUBKEY_HASH = None  # 暂时不启用，等你获取到再改

def get_random_nonce(length=16):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

class PinnedHttpAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        if EXPECTED_PUBKEY_HASH:
            def verify_callback(conn, cert, errno, depth, preverify_ok):
                if not preverify_ok:
                    return False
                pubkey = cert.public_key().public_bytes(
                    encoding=ssl.Encoding.DER,
                    format=ssl.PublicFormat.SubjectPublicKeyInfo
                )
                pubkey_hash = hashlib.sha256(pubkey).hexdigest()
                return pubkey_hash == EXPECTED_PUBKEY_HASH
            ctx.set_verify(ssl.VERIFY_PEER, verify_callback)
        ctx.check_hostname = bool(EXPECTED_PUBKEY_HASH)
        kwargs['ssl_context'] = ctx
        super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', PinnedHttpAdapter())

def call_activate_api(key, device_id, proxy_template, secret_key):
    timestamp = int(time.time())
    nonce = get_random_nonce()
    sign_str = f"{key}{device_id}{timestamp}{nonce}{proxy_template}"
    sign = hmac.new(secret_key, sign_str.encode(), 'sha256').hexdigest()
    payload = {
        "key": key,
        "device_id": device_id,
        "timestamp": timestamp,
        "nonce": nonce,
        "proxy_template": proxy_template,
        "sign": sign
    }
    try:
        resp = session.post(SERVER_URL, json=payload, timeout=10)
        return resp.json()
    except Exception as e:
        return {"code": 500, "message": f"网络错误: {str(e)}"}

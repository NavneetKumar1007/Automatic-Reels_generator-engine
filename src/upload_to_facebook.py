import requests

def upload_reel_to_facebook(page_id, page_access_token, video_path, caption):
    """
    Uploads a reel to a Facebook Page using Graph API v17+.
    Works even when the app is in Developer Mode (Admin only).
    """

    url = f"https://graph.facebook.com/v17.0/{page_id}/videos"

    print("🚀 Uploading reel to Facebook...")

    files = {
        "source": open(video_path, "rb")
    }

    data = {
        "access_token": page_access_token,
        "description": caption
    }

    response = requests.post(url, files=files, data=data)

    print("📌 Facebook Response:", response.status_code)
    print("📌 Response Text:", response.text)

    if response.status_code == 200:
        print("✅ Uploaded successfully to Facebook!")
    else:
        print("❌ Upload failed. Check error above.")


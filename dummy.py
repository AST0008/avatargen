import requests
key = "sk_V2_hgu_k2oGOq8IZ5C_qAM4vec0OtyoIEH7dte6utE5ZFhonF06"
# url = "https://api.heygen.com/v2/video/generate"
# headers = {
#     "X-Api-Key": key,
#     "Content-Type": "application/json"
# }
# payload = {
#     "video_inputs": [
#         {
#             "character": {
#                 "type": "talking_photo",
#                 # "avatar_id": "Daisy-inskirt-20220818",
#                 "talking_photo_id":"cbda5c4966534d8f8e3f300f828b0ae8"
#                 # "avatar_style": "normal"
#             },
#             "voice": {
#                 "type": "text",
#                 "input_text": "Hello world from ashwajit",
#                 "voice_id": "715e7730f62043c290be79876b19f692"
#             }
#         }
#     ],
#     "dimension": {
#         "width": 1280,
#         "height": 720
#     }
# }
# resp = requests.post(url, headers=headers, json=payload)
# print(resp.status_code, resp.text)



# url = "https://api.heygen.com/v1/streaming/avatar.list"
# headers = {"X-Api-Key": key}
# resp = requests.get(url, headers=headers)

# print("Status:", resp.status_code)
# print("Headers:", resp.headers)
# print("Raw text:", resp.text)   




import requests

# url = "https://api.heygen.com/v2/video.create"
# headers = {"Authorization": f"Bearer {key}"}

# payload = {
#     "talking_photo_id": "2411df8bdb0d40b088aa453d4c2a2d20",  # from talking_photos.list
#     "script": {
#         "type": "text",
#         "input": "Hello world, testing HeyGen Talking Photo!"
#     },
#     "background": {"type": "color", "value": "#ffffff"},
#     "dimension": {"width": 512, "height": 512}
# }

# resp = requests.post(url, headers=headers, json=payload)
# print("Status:", resp.status_code)
# print("Headers:", resp.headers)
# print("Text:", resp.text)


import requests

url = "https://api.heygen.com/v2/voices"

headers = {
    "accept": "application/json",
    "x-api-key": key
}

response = requests.get(url, headers=headers)

print(response.text)
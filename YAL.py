from googleapiclient.discovery import build

# Remplacez par votre clé API
API_KEY = "VOTRE_CLE_API"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_subscriptions(api_key):
    """Récupère les abonnements d'un compte YouTube."""
    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=api_key)
    
    subscriptions = []
    next_page_token = None

    while True:
        request = youtube.subscriptions().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response["items"]:
            channel_title = item["snippet"]["title"]
            channel_url = f"https://www.youtube.com/channel/{item['snippet']['resourceId']['channelId']}"
            subscriptions.append((channel_title, channel_url))
        
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    
    return subscriptions

def main():
    print("Récupération des abonnements...")
    subscriptions = get_subscriptions(API_KEY)

    with open("subscriptions.txt", "w", encoding="utf-8") as f:
        for title, url in subscriptions:
            f.write(f"{title}: {url}\n")
    
    print(f"Abonnements enregistrés dans 'subscriptions.txt'.")
    print("Vous pouvez maintenant les réinscrire manuellement sur un autre compte.")

if __name__ == "__main__":
    main()

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_authenticated_service():
    """Authentifie l'utilisateur via OAuth 2.0 et retourne le service YouTube."""
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Désactive HTTPS pour les tests locaux

    # Chemin vers vos identifiants OAuth 2.0
    CLIENT_SECRETS_FILE = "client_secret.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES
    )
    # Utilisez run_local_server() à la place de run_console()
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube

def get_subscriptions(youtube):
    """Récupère les abonnements d'un compte YouTube."""
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
    print("Authentification...")
    youtube = get_authenticated_service()
    print("Récupération des abonnements...")
    subscriptions = get_subscriptions(youtube)

    with open("subscriptions.txt", "w", encoding="utf-8") as f:
        for title, url in subscriptions:
            f.write(f"{title}: {url}\n")

    print("Abonnements enregistrés dans 'subscriptions.txt'.")

if __name__ == "__main__":
    main()

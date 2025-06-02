# app.py
import os
import requests
from flask import Flask, render_template, redirect, url_for, request, jsonify
from dotenv import load_dotenv
import stripe

# -----------------------------------------------------------------------------
# Load environment variables from .env
# -----------------------------------------------------------------------------
load_dotenv()
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
FLASK_SECRET_KEY = os.getenv("SECRET_KEY")

# -----------------------------------------------------------------------------
# Initialize Flask and Stripe
# -----------------------------------------------------------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY

# -----------------------------------------------------------------------------
# -- Helper: Fetch Instagram posts (Basic Display API) -----------------------
# -----------------------------------------------------------------------------
def fetch_instagram_posts(limit=6):
    """
    Fetches the latest `limit` posts from Instagram Basic Display API.
    Returns a list of dicts: { 'id', 'media_type', 'media_url', 'caption', 'timestamp' }.
    """
    if not INSTAGRAM_ACCESS_TOKEN:
        return []
    url = (
        f"https://graph.instagram.com/me/media"
        f"?fields=id,media_type,media_url,caption,timestamp,permalink"
        f"&access_token={INSTAGRAM_ACCESS_TOKEN}"
        f"&limit={limit}"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        # Optionally, reformat caption or thumbnail here
        return data
    except Exception as e:
        print("Error fetching Instagram posts:", e)
        return []

# -----------------------------------------------------------------------------
# -- Dummy Data: Team Members -------------------------------------------------
# -----------------------------------------------------------------------------
TEAM_MEMBERS = [
    {
        "name": "Diego Alonso",
        "role": "Founder & Lead Guide",
        "photo": "images/team/diego.jpg",
        "bio": "Data scientist turned traveler, passionate about sustainable tourism.",
        "interests": ["Wildlife photography", "AI for conservation", "Football"],
    },
    {
        "name": "Yumi Tanaka",
        "role": "Operations Manager",
        "photo": "images/team/yumi.jpg",
        "bio": "Ensures every tour runs smoothly and sustainably.",
        "interests": ["Hiking", "Local cuisine", "Cultural exchanges"],
    },
    {
        "name": "Markus Schmidt",
        "role": "Lead Photographer",
        "photo": "images/team/markus.jpg",
        "bio": "Capturing Japan’s hidden corners one frame at a time.",
        "interests": ["Photography", "Bird watching", "Cycling"],
    },
    # Add more members as needed...
]

# -----------------------------------------------------------------------------
# -- Dummy Data: Tours (organized by season) ----------------------------------
# -----------------------------------------------------------------------------
# Each tour: title, slug, image, short_desc, price, details (HTML-friendly text)
TOURS_BY_SEASON = {
    "spring": [
        {
            "title": "Cherry Blossoms & Countryside Cycling",
            "slug": "cherry-cycling",
            "image": "images/tours/spring_cherry.jpg",
            "short_desc": "Pedal through small towns beneath pink sakura canopies.",
            "price": 120.00,
            "details": "Experience rural Japan at its most beautiful, with local homestays and authentic cuisine.",
        },
        {
            "title": "Mount Fuji Yamanashi Hidden Path Trek",
            "slug": "fuji-hidden-trek",
            "image": "images/tours/spring_fuji.jpg",
            "short_desc": "Beat the crowds and see Mt. Fuji from secret vantage points.",
            "price": 150.00,
            "details": "A 2-day guided trek with nights in traditional inns, focusing on sustainability and minimal impact.",
        },
        # Add up to 4 tours for spring...
    ],
    "summer": [
        {
            "title": "Lake Tanuki & Fujinomiya Shrine Day Trip",
            "slug": "lake-tanuki-fujinomiya",
            "image": "images/tours/summer_lake_tanuki.png",
            "short_desc": "Visit Lake Tanuki with Fuji views, rent a rowboat, then Fujisan Hongū Sengen Shrine and return to Shinjuku.",
            "price": 7480.00,
            "details": (
                "07:00 depart Shinjuku by highway bus to Lake Tanuki (¥4000). "
                "11:00–12:30 explore the lake, rent a rowboat to see the “double diamond Fuji”. "
                "12:30–13:30 lunch at Kyukamura Tanuki lakeside café or a local udon shop; try Fujinomiya yakisoba. "
                "13:35 take bus (¥880) from Lake Tanuki to Fujisan Hongū Sengen Shrine (UNESCO World Heritage). "
                "15:00 return from Nishifujinomiya to Shinjuku via Shin-Fuji (Shinkansen Kodama or JR Tōkaidō, ¥2600), arriving around 18:30."
            ),
        },
        {
            "title": "Nokogiriyama & Futtsu Coastal Adventure",
            "slug": "nokogiriyama-futtsu",
            "image": "images/tours/summer_nokogiriyama.jpg",
            "short_desc": "Ferry to Nokogiriyama for a mountain hike and giant Buddha, then visit Cape Futtsu Park with Mt. Fuji views.",
            "price": 3728.00,
            "details": (
                "07:30 depart Shinagawa → Keikyū Kurihama (¥710). "
                "08:15–08:30 walk (~20 min) to Kurihama Ferry Port, ferry to Kanaya (¥890). "
                "09:00–10:30 hike Nokogiriyama: see Hyaku-shaku Kannon and the 31.5 m Buddha statue. "
                "11:00 picnic lunch at the mountain top. "
                "11:45 descend. "
                "12:30–14:00 train from Hamakanaya → Sanukimachi, then bus to Futtsu Port (~¥610 total). "
                "Visit Cape Futtsu Park for a seaside walk and Mt. Fuji views. "
                "14:30 train from Aohori → Tokyo (¥1518), returning by mid-afternoon."
            ),
        },
        {
            "title": "Nagatoro River & Hodosan Shrine Excursion",
            "slug": "nagatoro-hodosan",
            "image": "images/tours/summer_nagatoro.jpg",
            "short_desc": "Experience river activities in Nagatoro Gorge and take the ropeway up to Hodosan Shrine.",
            "price": 2100.00,
            "details": (
                "08:00 take Seibu Limited Express from Ikebukuro → Seibu-Chichibu, upgrade for Nagatoro (Seibu 1-Day Pass + Nagatoro upgrade: ¥1500). "
                "10:00–12:00 enjoy Nagatoro Gorge: choose a yakata-bune boat (approx. ¥3000) or whitewater raft ride, or rent a rowboat (¥2000) near Iwadatami Rocks. "
                "12:15–13:15 lunch in Nagatoro town (river fish curry or river trout sashimi). "
                "13:30 visit Hodosan Shrine; ride Nagatoro Hodosan Ropeway (¥600 round-trip) to the summit of Mt. Hodo. "
                "15:30 walk back down, sampling local Mitsumine soba or wagashi. "
                "16:30 return by Seibu/Nagatoro train to Ikebukuro, arriving around 18:30."
            ),
        },
    ],
    "autumn": [
        {
            "title": "Hidden Temples of Kyoto (Off-Peak)",
            "slug": "kyoto-hidden",
            "image": "images/tours/autumn_kyoto.jpg",
            "short_desc": "Explore small, less-crowded shrines & teahouses.",
            "price": 130.00,
            "details": "Local monk guides you through secret gardens during autumn foliage season.",
        },
        # ...
    ],
    "winter": [
        {
            "title": "Snow Monkeys & Nagano Village Stay",
            "slug": "nagano-monkeys",
            "image": "images/tours/winter_nagano.jpg",
            "short_desc": "Watch macaques bathing in hot springs—no tourist bus in sight.",
            "price": 160.00,
            "details": "Stay in a ryokan, enjoy local onsen, and support villagers directly.",
        },
        # ...
    ],
}


# -----------------------------------------------------------------------------
# -- ROUTES --------------------------------------------------------------------
# -----------------------------------------------------------------------------
@app.route("/")
def index():
    # For the landing page, you might want to show a few featured tours (e.g., top 3)
    featured = []
    for season, tours in TOURS_BY_SEASON.items():
        featured.extend(tours[:1])  # take first tour from each season
    return render_template("index.html", featured_tours=featured)

@app.route("/about")
def about():
    return render_template("about.html", team=TEAM_MEMBERS)

@app.route("/blog")
def blog():
    posts = fetch_instagram_posts(limit=8)
    # Reformat each post’s caption if desired, e.g., truncate or style differently
    return render_template("blog.html", posts=posts)

@app.route("/tours")
def tours():
    # Pass the entire TOURS_BY_SEASON dict to the template
    return render_template("tours.html", tours_by_season=TOURS_BY_SEASON)

@app.route("/tours/<season>/<slug>")
def tour_detail(season, slug):
    season = season.lower()
    tours = TOURS_BY_SEASON.get(season, [])
    for tour in tours:
        if tour["slug"] == slug:
            return render_template("tour_detail.html", season=season, tour=tour, stripe_pk=STRIPE_PUBLISHABLE_KEY)
    return "Tour not found", 404

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    """
    Expects JSON: { 'tour_slug': '...', 'season': '...' }
    Finds the tour price, creates a Stripe Checkout session, and returns the URL.
    """
    data = request.get_json()
    season = data.get("season")
    slug = data.get("tour_slug")
    # Look up the tour
    tour = next(
        (t for t in TOURS_BY_SEASON.get(season, []) if t["slug"] == slug),
        None,
    )
    if not tour:
        return jsonify({"error": "Tour not found"}), 404

    # Create a Stripe Checkout session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": tour["title"],
                        "description": tour["short_desc"],
                    },
                    "unit_amount": int(tour["price"] * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=request.host_url + "success",
            cancel_url=request.host_url + f"tours/{season}/{slug}",
        )
        return jsonify({"id": checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/success")
def success():
    return "<h1>Thank you for your booking!</h1><p>Your payment was successful.</p>"

# -----------------------------------------------------------------------------
# Run the app
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # When running locally, Flask will detect debug mode via FLASK_ENV=development
    app.run(host="0.0.0.0", port=5000)

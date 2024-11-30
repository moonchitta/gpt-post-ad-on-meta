import os

import requests
from dotenv import load_dotenv
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize API with credentials from environment variables
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")

FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)

@app.route('/')
def home():
    """Homepage for the Meta API application."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to Meta API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
                background-color: #f4f4f9;
            }
            header {
                text-align: center;
                margin-bottom: 20px;
            }
            footer {
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #777;
            }
            .content {
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background: #fff;
                border: 1px solid #ddd;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Welcome to the Meta API Service</h1>
        </header>
        <div class="content">
            <p>This application allows you to interact with the Meta (Facebook/Instagram) Ads API.</p>
            <h2>Available Endpoints:</h2>
            <ul>
                <li><b>POST /create_campaign</b>: Create a new campaign.</li>
                <li><b>POST /create_ad_set</b>: Create an ad set for a campaign.</li>
                <li><b>POST /create_ad_creative</b>: Create an ad creative.</li>
                <li><b>POST /create_ad</b>: Create an ad for a specific ad set and creative.</li>
                <li><b>GET /get_campaign_insights</b>: Fetch insights for a specific campaign.</li>
            </ul>
            <p>Use these endpoints to manage your advertising campaigns programmatically.</p>
        </div>
        <footer>
            &copy; 2024 TheXSol.com
        </footer>
    </body>
    </html>
    """
    return html_content


@app.route('/create_campaign', methods=['POST'])
def create_campaign():
    """Endpoint to create an ad campaign."""
    try:
        # Parse input data
        data = request.json
        campaign_name = data.get('campaign_name', 'Default Campaign')
        objective = data.get('objective', 'APP_INSTALLS')  # Default objective
        status = data.get('status', 'PAUSED')  # Default to PAUSED
        special_ad_categories = data.get('special_ad_categories', [])  # Default to empty

        # Additional parameters (if provided)
        buying_type = data.get('buying_type')  # Optional: e.g., AUCTION
        campaign_budget_optimization = data.get('campaign_budget_optimization')  # Optional
        spend_cap = data.get('spend_cap')  # Optional

        # Build campaign parameters dynamically
        campaign_params = {
            'name': campaign_name,
            'objective': objective,
            'status': status,
            'special_ad_categories': special_ad_categories,
        }

        # Add optional parameters if provided
        if buying_type:
            campaign_params['buying_type'] = buying_type
        if campaign_budget_optimization is not None:
            campaign_params['campaign_budget_optimization'] = campaign_budget_optimization
        if spend_cap:
            campaign_params['spend_cap'] = spend_cap

        # Create the campaign
        ad_account = AdAccount(AD_ACCOUNT_ID)
        campaign = ad_account.create_campaign(params=campaign_params)

        # Return success response
        return jsonify({
            'message': 'Campaign created successfully',
            'campaign_id': campaign['id']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_ad_set', methods=['POST'])
def create_ad_set():
    """Endpoint to create an ad set for page promotion."""
    try:
        # Parse input data
        data = request.json
        campaign_id = data.get('campaign_id')
        name = data.get('name', 'Default Ad Set')
        daily_budget = data.get('daily_budget', 100000)  # Default PKR 1,000 in paisa
        bid_amount = data.get('bid_amount', 5000)  # Default PKR 50 in paisa
        geo_locations = data.get('geo_locations', {'countries': ['PK']})  # Default to Pakistan
        facebook_positions = data.get('facebook_positions', ['feed'])  # Default placement
        promoted_object = data.get('promoted_object', {})
        optimization_goal = data.get('optimization_goal', 'PAGE_LIKES')  # Default goal
        billing_event = data.get('billing_event', 'IMPRESSIONS')  # Default billing event
        status = data.get('status', 'PAUSED')  # Default to PAUSED

        # Validate required fields
        if not campaign_id:
            return jsonify({'error': 'campaign_id is required'}), 400
        if not promoted_object.get('page_id'):
            return jsonify({'error': 'promoted_object.page_id is required for page promotion'}), 400

        # Define targeting structure
        targeting = {
            'geo_locations': geo_locations,
            'facebook_positions': facebook_positions,
        }

        # Create the ad set
        ad_account = AdAccount(AD_ACCOUNT_ID)
        params = {
            'name': name,
            'campaign_id': campaign_id,
            'daily_budget': daily_budget,
            'billing_event': billing_event,
            'optimization_goal': optimization_goal,
            'bid_amount': bid_amount,
            'targeting': targeting,
            'status': status,
            'promoted_object': promoted_object
        }

        print(f"Params: {params}")

        ad_set = ad_account.create_ad_set(params=params)

        # Return success response
        return jsonify({
            'message': 'Ad Set created successfully',
            'ad_set_id': ad_set['id']
        })
    except Exception as e:
        # Log the error for debugging
        print(f"Error creating ad set: {e}")
        return jsonify({'error': str(e)}), 500


def upload_image_and_get_hash(image_url):
    """
    Downloads an image from the provided URL and uploads it to Meta's Ads API.
    Returns the image hash after the upload.

    :param image_url: The URL of the image to be uploaded.

    :return: image_hash (str) if successful, or error message if failed.
    """
    try:
        # Step 1: Download the image
        print(f"Downloading image from {image_url}")
        image_response = requests.get(image_url)

        if image_response.status_code != 200:
            return f"Error: Failed to download image from URL {image_url}", None

        print(f"Image downloaded successfully")

        # Step 2: Prepare the image for upload (multipart/form-data)
        files = {
            'file': ('image.jpg', image_response.content)  # The image content as bytes
        }

        # Step 3: Upload the image to Meta's Ads API
        image_upload_url = f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/adimages"
        params = {
            'access_token': ACCESS_TOKEN  # Authentication using the access token
        }

        # Send the POST request to upload the image
        upload_response = requests.post(image_upload_url, files=files, params=params)

        print(f"upload_response: {upload_response.json()}")

        # Step 4: Handle the response and extract image hash
        if upload_response.status_code == 200:
            image_upload_data = upload_response.json()  # Parse the response JSON
            image_hash = image_upload_data['images']['image.jpg']['hash']  # Extract the image hash
            return None, image_hash  # Return None for success and the image_hash
        else:
            return f"Error: {upload_response.json()}", None  # Return error message if failed

    except Exception as e:
        return f"Error occurred: {str(e)}", None  # Return error message in case of an exception

@app.route('/create_ad_creative', methods=['POST'])
def create_ad_creative():
    """Endpoint to create an ad creative with an image URL or image hash."""
    try:
        data = request.json

        # Required fields
        page_id = data.get('page_id')
        link = data.get('link')
        image_url = data.get('image_url')  # URL of the image to upload
        image_hash = data.get('image_hash')  # Precomputed image hash

        # Optional fields
        message = data.get('message', 'Check out our latest updates!')
        call_to_action_type = data.get('call_to_action_type', 'LEARN_MORE')
        creative_name = data.get('creative_name', 'Default Ad Creative')
        enroll_status = data.get('enroll_status', 'not_enrolled')  # Default to not enrolled

        # Validate required fields
        if not page_id:
            return jsonify({'error': 'page_id is required'}), 400
        if not link:
            return jsonify({'error': 'link is required'}), 400
        if not (image_url or image_hash):
            return jsonify({'error': 'Either image_url or image_hash is required'}), 400

        ad_account = AdAccount(AD_ACCOUNT_ID)
        # Step 1: Upload the image and get image_hash (if image_url is provided)
        if not image_hash and image_url:
            # print(f"Downloading image from {image_url}")
            # image_response = requests.get(image_url)
            # if image_response.status_code != 200:
            #     return jsonify({'error': 'Failed to download image from the provided URL'}), 400
            #
            # print(f"Image downloaded")
            # # Upload the image to Meta
            # image_data = {
            #      'file', image_response.content
            # }
            # image_upload_response = ad_account.create_ad_image(params=image_data)
            # print(f"Image Uploaded {image_upload_response}")
            # image_hash = image_upload_response['hash']

            # Call the method to upload the image and get the image hash
            error, image_hash = upload_image_and_get_hash(image_url)

            if error:
                print(f"Error: {error}")
                return jsonify({'error': 'Failed to download image from the provided URL'}), 400
            else:
                print(f"Image uploaded successfully. Image Hash: {image_hash}")

        print(f"Hash of image: {image_hash}")

        # Step 2: Create the ad creative
        creative_data = {
            'name': creative_name,
            'object_story_spec': {
                'page_id': page_id,
                'link_data': {
                    'link': link,
                    'message': message,
                    'image_hash': image_hash,
                    'call_to_action': {
                        'type': call_to_action_type
                    }
                }
            },
            'degrees_of_freedom_spec': {
                'creative_features_spec': {
                    'standard_enhancements': {
                        'enroll_status': enroll_status
                    }
                }
            }
        }
        creative = ad_account.create_ad_creative(params=creative_data)

        return jsonify({
            'message': 'Ad Creative created successfully',
            'creative_id': creative['id']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/create_ad', methods=['POST'])
def create_ad():
    """Endpoint to create an ad."""
    try:
        data = request.json

        # Required fields
        ad_set_id = data.get('ad_set_id')
        creative_id = data.get('creative_id')

        # Optional fields
        ad_name = data.get('ad_name', 'Default Ad')

        # Validate required fields
        if not ad_set_id:
            return jsonify({'error': 'ad_set_id is required'}), 400
        if not creative_id:
            return jsonify({'error': 'creative_id is required'}), 400

        # Create the ad
        ad_account = AdAccount(AD_ACCOUNT_ID)
        ad = ad_account.create_ad(params={
            'name': ad_name,
            'adset_id': ad_set_id,
            'creative': {'creative_id': creative_id},
            'status': 'PAUSED'  # Set to 'ACTIVE' if the ad should run immediately
        })

        return jsonify({
            'message': 'Ad created successfully',
            'ad_id': ad['id']
        })
    except Exception as e:
        # Return detailed error response
        return jsonify({'error': str(e)}), 500

@app.route('/update_campaign_status', methods=['POST'])
def update_campaign_status():
    """Endpoint to update a campaign's status."""
    try:
        data = request.json
        campaign_id = data.get('campaign_id')
        new_status = data.get('status', 'ACTIVE')  # Default to 'ACTIVE'

        if not campaign_id:
            return jsonify({'error': 'campaign_id is required'}), 400

        # Update campaign status
        campaign = Campaign(fbid=campaign_id)
        campaign.api_update(params={'status': new_status})

        return jsonify({
            'message': f'Campaign status updated to {new_status}',
            'campaign_id': campaign_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_campaigns', methods=['GET'])
def get_campaigns():
    """Endpoint to fetch the list of current campaigns."""
    try:
        ad_account = AdAccount(AD_ACCOUNT_ID)
        campaigns = ad_account.get_campaigns(fields=[
            Campaign.Field.id,
            Campaign.Field.name,
            Campaign.Field.status
        ])

        # Format response
        campaign_list = [
            {'id': campaign[Campaign.Field.id],
             'name': campaign[Campaign.Field.name],
             'status': campaign[Campaign.Field.status]}
            for campaign in campaigns
        ]

        return jsonify({
            'message': 'Campaigns fetched successfully',
            'campaigns': campaign_list
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
# **Facebook Ads API Integration with Python** 🎯

This project provides a **Python-based API** to interact with **Facebook Ads API**. It allows you to automate the process of creating campaigns, ad sets, ad creatives, and ads. Additionally, this API can be used in conjunction with **ChatGPT Actions** to execute Facebook Ads-related tasks programmatically.

---

## **Features** 🔧

- **Create Campaigns**: Create Facebook ad campaigns by defining objectives, budget, and status.
- **Create Ad Sets**: Create ad sets within campaigns with targeting parameters, budgets, and bid amounts.
- **Create Ad Creatives**: Upload images and generate ad creatives with the required configurations.
- **Create Ads**: Combine the ad creative and ad set to create the final ad.
- **Integration with ChatGPT Actions**: Allow interaction with the API using ChatGPT, making it possible to create ads with natural language commands.

---

## **Setup and Installation** 💻

1. **Clone the repository**:

```bash
git clone https://github.com/moonchitta/gpt-post-ad-on-meta
cd gpt-post-ad-on-meta
```

2. **Install dependencies**:

Make sure you have **Python 3.x** installed, and install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

The required libraries include:
- **Flask**: A lightweight web framework to build the API.
- **facebook-business**: Official SDK to interact with Facebook's Marketing API.
- **python-dotenv**: For securely loading API keys and credentials from `.env` file.

3. **Create a `.env` file** in the root directory with your credentials:

```bash
ACCESS_TOKEN=your-facebook-access-token
APP_ID=your-facebook-app-id
APP_SECRET=your-facebook-app-secret
AD_ACCOUNT_ID=your-facebook-ad-account-id
```

4. **Run the Flask Application**:

```bash
python app.py
```

This will start the Flask application on `http://localhost:5000`.

---

## **API Endpoints** 📡

Below is a list of available endpoints to interact with the API:

### **1. `/create_campaign`** [POST]
- **Description**: Create a new campaign in your Facebook Ad Account.
- **Request Body**:
    ```json
    {
      "campaign_name": "My Campaign",
      "objective": "OUTCOME_ENGAGEMENT",
      "status": "PAUSED",
      "special_ad_categories": [],
      "buying_type": "AUCTION",
      "campaign_budget_optimization": true,
      "spend_cap": 10000
    }
    ```

### **2. `/create_ad_set`** [POST]
- **Description**: Create an ad set under a specific campaign.
- **Request Body**:
    ```json
    {
      "campaign_id": "120212200922490587",
      "name": "Ad Set Name",
      "daily_budget": 105000,
      "bid_amount": 5000,
      "geo_locations": {"countries": ["PK"]},
      "facebook_positions": ["feed"],
      "promoted_object": {"page_id": "564302590654103"},
      "optimization_goal": "PAGE_LIKES",
      "billing_event": "IMPRESSIONS",
      "status": "PAUSED"
    }
    ```

### **3. `/create_ad_creative`** [POST]
- **Description**: Upload an image and create an ad creative.
- **Request Body**:
    ```json
    {
      "page_id": "564302590654103",
      "link": "https://www.thexsol.com",
      "image_url": "https://upload.wikimedia.org/wikipedia/en/0/0d/PiL_Public_Image.jpg",
      "message": "Check out our latest updates!",
      "call_to_action_type": "LEARN_MORE",
      "creative_name": "Default Ad Creative",
      "enroll_status": "OPT_IN"
    }
    ```

### **4. `/create_ad`** [POST]
- **Description**: Create an ad with the provided ad set and creative.
- **Request Body**:
    ```json
    {
      "ad_set_id": "your-ad-set-id",
      "creative_id": "your-creative-id",
      "ad_name": "Ad Name",
      "status": "PAUSED"
    }
    ```

---

## **Using ChatGPT Actions** 🤖

You can use **ChatGPT Actions** to interact with this API. For example, you can instruct ChatGPT to perform tasks like creating ads, updating campaigns, or uploading images. 

To integrate this with **ChatGPT**:
1. Set up **Custom GPT** through OpenAI’s platform.
2. In the **Actions Configuration**, link the appropriate API endpoints. For example, you can allow ChatGPT to **POST** requests to `/create_campaign`, `/create_ad_set`, and other endpoints to create ads.
3. ChatGPT will prompt you for the required inputs (e.g., campaign name, budget, etc.), and then send the request to the API.

### **Example**:
In ChatGPT, you can provide a prompt like:

> **"Create a new ad campaign named 'My Ad Campaign' with the objective 'OUTCOME_ENGAGEMENT', a daily budget of 1000, and PAUSED status."**

ChatGPT can interpret this request and call the **`/create_campaign`** API, handling the interaction automatically.

---

## **Running the Application with ChatGPT** 🤝

1. **Set up ChatGPT to call your Flask API** by providing the required API URL and endpoint.
2. **Configure the environment** (i.e., API keys and URLs) in ChatGPT’s prompt engineering section or through the backend integration.
3. **Execute Commands**: Once set up, ChatGPT will automatically send the commands to the API and retrieve the results.

For instance, the response from the `/create_campaign` endpoint might be:

```json
{
  "message": "Campaign created successfully",
  "campaign_id": "120212200922490587"
}
```

---

## **Example Interaction with ChatGPT**:

1. **User Input**: 
   > "Create a campaign called 'Summer Sale' with an objective of 'OUTCOME_ENGAGEMENT' and a budget of 5000."

2. **ChatGPT API Call**: 
   - ChatGPT sends a **POST** request to `/create_campaign` with the provided parameters.
   
3. **ChatGPT Output**:
   > "Your campaign 'Summer Sale' has been created successfully. Campaign ID: 120212200922490587."

---

## **Contributing** 💡

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes and commit them.
4. Open a pull request with a description of the changes.

---

## **License** 📜

This project is licensed under the **MIT License**.

---

### **Conclusion** 🎉

This project allows you to easily integrate **Facebook Ads** with Python. By using **Flask** to expose API endpoints and integrating them with **ChatGPT Actions**, you can seamlessly automate your Facebook Ads management, creating campaigns, ad sets, creatives, and ads, all through conversational commands.

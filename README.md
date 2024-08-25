# Stellarmark Background Remover Bot

Stellarmark Background Remover Bot is a powerful Telegram bot designed to help you easily remove the background from your images. Built with Python, this bot leverages cutting-edge image processing libraries to deliver fast and accurate results. Whether you want to clean up a profile picture or create a transparent image, Stellarmark has you covered.

## 🚀 Features

- **Automatic Background Removal**: Upload any image, and the bot will remove the background for you in seconds.
- **Referral System**: Invite friends to use the bot and increase your daily processing quota.
- **Inline Mode**: Use the bot directly in any chat by typing `@your_bot_username` to quickly remove backgrounds from images.
- **Daily Quota Management**: Manage your daily image processing limit, which can be expanded through referrals.
- **Statistics**: Keep track of your usage and referral stats.

## 🛠 Installation

To set up and run the Stellarmark Background Remover Bot locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/abelzk/StellarMark-Backgroud-Remover-Bot.git
cd stellarmark-bg-remover-bot
    ```

2. **Install the dependencies:**

 ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    Create a `.env` file in the root directory of the project and add the following environment variables:

    ```env
    BOT_TOKEN=your-telegram-bot-token
    BOT_USERNAME=your-bot-username
    CHANNEL_PRIVATE_LINK=your-channel-private-link
    API_KEY=your-sqlitecloud-api-key
    ```

4. **Run the bot:**

    ```bash
    python bot.py
    ```

## 📋 Commands
   ```bash
- `/start` - Start the bot and register a new user.
- `/help` - Display help information on how to use the bot.
- `/usage` - Display your current usage statistics.
- `/referral` - Display your referral information and link.
- `/stats` - Display overall bot statistics (only available to the bot admin).
   ```

## 📌 Usage Guide

1. **Send an Image:** Simply send an image to the bot, and it will return the image with the background removed.

2. **Referral Program:** When you register, you will receive a unique referral link. Share this link with friends to earn additional image processing quotas.

3. **Inline Queries:** Use the bot in any chat by typing `@your_bot_username` followed by your query to quickly remove backgrounds from images.

## 🛠 Technologies Used

- **Python**: The primary language for the bot.
- **Telegram Bot API**: Used to interact with Telegram users.
- **rembg**: A Python library used to remove image backgrounds.
- **sqlitecloud**: Cloud-based SQLite database for storing user data.
- **Pillow**: Python Imaging Library (PIL) for image processing.
- **httpx**: HTTP client for asynchronous requests.

## 📊 Statistics

- **Total Users:** View the number of registered users.
- **Total Images Processed:** Track how many images have been processed by the bot.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to fork the repository, create a branch, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## Contact

For any inquiries or support, reach out to [Abel Zecharias](mailto:abelzeki24@gmail.com)

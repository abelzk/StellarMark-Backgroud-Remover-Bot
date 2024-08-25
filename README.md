# Stellarmark Background Remover Bot

Stellarmark Background Remover Bot is a Telegram bot that allows users to remove the background from images. The bot is built with Python and leverages the `rembg` library for background removal. Users can interact with the bot via direct commands, image uploads, or inline queries. Additionally, the bot offers a referral system that rewards users with additional image processing quotas for each successful referral.

## Features

- **Image Background Removal:** Upload an image, and the bot will remove the background for you.
- **Referral System:** Invite friends to use the bot and increase your daily processing quota.
- **Inline Queries:** Use the bot inline to quickly remove backgrounds from images shared in any chat.
- **Daily Quota:** Each user has a daily quota of images they can process. This quota can be increased via referrals.
- **Usage Statistics:** View your current usage statistics, including your daily quota, images processed, and referral status.

## Installation

To run this bot locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/stellarmark-bg-remover-bot.git
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

## Commands

- `/start` - Start the bot and register a new user.
- `/help` - Display help information on how to use the bot.
- `/usage` - Display your current usage statistics.
- `/referral` - Display your referral information and link.
- `/stats` - Display overall bot statistics (only available to the bot admin).

## Usage

1. **Send an Image:** Simply send an image to the bot, and it will return the image with the background removed.

2. **Referral Program:** When you register, you will receive a unique referral link. Share this link with friends to earn additional image processing quotas.

3. **Inline Queries:** Use the bot in any chat by typing `@your_bot_username` followed by your query to quickly remove backgrounds from images.

## Technologies Used

- **Python**: The primary language for the bot.
- **Telegram Bot API**: Used to interact with Telegram users.
- **rembg**: A Python library used to remove image backgrounds.
- **sqlitecloud**: Cloud-based SQLite database for storing user data.
- **Pillow**: Python Imaging Library (PIL) for image processing.
- **httpx**: HTTP client for asynchronous requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to suggest improvements.

## Contact

For any inquiries or support, reach out to [Abel Zecharias](mailto:abelzeki24@gmail.com)

import Constants as keys
from telegram.ext import *
from summarizer import SummaryArticle


print("Bot started...")

summary_article = SummaryArticle()


def handle_message(update, context):
    text = str(update.message.text).lower()

    number_of_sentences = len(text.split("."))

    if number_of_sentences >= 2:
        response = summary_article.summarize(text)

    else:
        response = summary_article.process(text)

    update.message.reply_text(response)


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher


    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

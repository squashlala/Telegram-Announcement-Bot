import subprocess
from datetime import datetime
from telegram import Update, Chat, Bot, Message   #Importting elements from the telegram-python-bot (to install them use in a cli "pip install python-telegram-bot")
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

str1=' ' #Used for parsing

helpMessage = """Bonjour humain ou anthropomorphe!
Je suis le robot qui permet d'annoncer les événements dans "Les Furs Rémois - Annonces événements".
Si tu veux faire connaître le tien tape dans le groupe : "/annonce [ton évènement]"

Merci de le mettre sous cette forme (tout message ne respectant pas cette forme sera refusé):
    /annonce Date et heure : dd/MM/yyyy hh:mm
    Lieu : [nom + addresse + lien google maps si besoin]
    Détails : [les détails de l'évenement]

Lien du channel : https://t.me/joinchat/VcOwtl0vOyUegiLr"""   #help message given with /aide
forbiddenMessage="Vous n'avez pas le droit d'utiliser ce bot, cette utilisation sera loggée @"   #Message given to people trying to command the bot from a non allowed chat

chatsID = [-1001449541957,-1001069715993]   #List of allowed chat ID -1001233252813
channelID = -1001438888118   #Announcement channel ID
logChannel = -1001337904666   #Logging channel ID

now = datetime.now()
currentTime= now.strftime("%d/%m/%Y %H:%M:%S")   #Getting current time (can be used for logging if not used in a channel)


#Def of the announcement
def announce(update: Update, context: CallbackContext) -> None:
    try:   #Trying to read the command and publish it
        if len(context.args) >> 0 and update.message.chat.id in chatsID:   #If the text following the command isn't empty and the chat ID is allowed
            if "Date et heure :" in update.effective_message.text and "\nLieu :" in update.effective_message.text and "\nDétails :" in update.effective_message.text:   #If the text following the command is properly formated
                eventBroadcast=update.effective_message.text+"\n\nProposé par : @"+update.message.from_user.username #The sender is added to the ennouncement
                eventBroadcast=eventBroadcast[9:]   #We get rid of the first 9 chars (representing "/annonce ")
                job = context.job
                context.bot.send_message(chat_id=channelID,text=eventBroadcast)   #We broadcast the announcement to the desired channel
                context.bot.send_message(chat_id=logChannel,text=" OK : @"+update.message.from_user.username+" in '"+update.message.chat.title+"' commanded : '"+str1.join(context.args)+"'\n")   #We log the announcement to the desired log channel
            else :   #If the format isn't respected the sender is replied to
                update.message.reply_text("Merci de respecter le format d'annonce @"+update.message.from_user.username)
                context.bot.send_message(chat_id=logChannel,text=" WARNING : @"+update.message.from_user.username+" in '"+update.message.chat.title+"' commanded in wrong format : '"+str1.join(context.args)+"'\n")   #The mistake is logged
        
        elif len(context.args) == 0 and update.message.chat.id in chatsID:   #If the text following the command is empty and the chat ID is allowed the sender is notified and the mistake is logged
            update.message.reply_text("Merci de préciser l'évènement @"+update.message.from_user.username)
            context.bot.send_message(chat_id=logChannel,text=" OK : @"+update.message.from_user.username+" in '"+update.message.chat.title+"' commanded : '"+str1.join(context.args)+"'\n")
        
        else:   #Otherwise, the sender is not allowed to use the bot
            update.message.reply_text(forbiddenMessage+update.message.from_user.username)
            context.bot.send_message(chat_id=logChannel,text=" CRITICAL : @"+update.message.from_user.username+" in '"+update.message.chat.title+"' commanded : '"+str1.join(context.args)+"' without permission...\n")
    except (IndexError, ValueError): #If the trial fails an error message is answered
        update.message.reply_text("Une erreur est survenue merci de réessayer @"+update.message.from_user.username)
        context.bot.send_message(chat_id=logChannel,text=" WARNING : @"+update.message.from_user.username+" in '"+update.message.chat.title+"' commanded : '"+str1.join(context.args)+"' it failed...\n")   #Tthe use is logged

#Def of the help
def help(update: Update, context: CallbackContext) -> None:
    if update.message.chat.id in chatsID:   #If the /help comes from an allowed chat the help is displayed
        update.message.reply_text(helpMessage)
    else :   #Otherwise, the sender is notified he can't use the bot
        update.message.reply_text("L'utilisation de ce bot est réservée à des groupes spécifiques.\nNéanmoins son code sera rendu disponible prochainement.")
        #print(update.message.chat.id)
        context.bot.send_message(chat_id=logChannel,text="Un chat non autorisé demande de l'aide :\n'"+update.message.chat.title+"' / "+str(update.message.chat.id))   #The use is logged

updater=Updater('1678111133:AAE9QOWPWBpoWi2hPVWuAKjJQ8pBHTrzFGI')   #Here we ggive the bot API tokens

updater.dispatcher.add_handler(CommandHandler('annonce', announce))   #If the /annonce command is received, we use the announce def
updater.dispatcher.add_handler(CommandHandler('aide', help))   #If the /aide command is received, we use the help def

updater.start_polling()   #Some stuff the bot needs to work
updater.idle()

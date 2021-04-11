#Python3.9 
import subprocess
from datetime import datetime
from telegram import Update, Chat, Bot, Message   #Importting elements from the telegram-python-bot (to install them use in a cli "pip install python-telegram-bot")
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

str1=' ' #Used for parsing

helpMessage = """Je suis le robot qui permet d'annoncer les évènements dans "Some Channel".
Si tu veux faire connaitre le tiens tape dans le groupe : "/annonce [ton évènement]"

Merci de le mettre sous cette forme (tout messages ne respectant pas la mise en forme serront refusés):
    /annonce Date et heure : dd/MM/yyyy hh:mm
    Lieu : [nom + addresse + lien google maps si besoin]
    Détails : [les détails de l'évenement]

Lien du channel : https://t.me/"""   #help message given with /aide
forbiddenMessage="Vous n'avez pas le droit d'utiliser ce bot, cette utilisation sera loggée @"   #Message given to people trying to command the bot from a non allowed chat

chatsID = [-nnnnnn,-mmmmmm]   #List of allowed chat ID 
channelID = -oooooo   #Announcement channel ID
logChannel = -pppppp   #Logging channel ID

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
        update.message.reply_text("L'utilisation de ce bot est réservé à des groupes spéciques.\nNéanmoins son code sera rendu disponible prochainement.")
        context.bot.send_message(chat_id=logChannel,text="ID du channel demandeur d'aide : "+update.message.chat.id)   #The use is logged


updater=Updater('your bot token')   #Here we ggive the bot API tokens

updater.dispatcher.add_handler(CommandHandler('annonce', announce))   #If the /annonce command is received, we use the announce def
updater.dispatcher.add_handler(CommandHandler('aide', help))   #If the /aide command is received, we use the help def

updater.start_polling()   #Some stuff the bot needs to work
updater.idle()

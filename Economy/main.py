from email import message
import discord
from discord.ext import commands
import json
import os
import random
import asyncio


client = commands.Bot

mainshop = [{"name":"Coke","price":100,"description":"Have fun :)"},{"name":"Watch","price":2500,"description":"Time"},{"name":"Laptop","price":5000,"description":"Work"},{"name":"PC","price":10000,"description":"Gaming"},{"name":"GPU","price":20000,"description":"Build a Bitcoin mining rig lol"},{"name":"House","price":100000,"description":"Home"}]

wallet_lim = 1000000000
bank_lim = 100000000

wallet_lim_msg = "U already hv the max amount of coins u can hv in ur wallet, bud."
bank_lim_msg = "U already hv the max amount of coins u can hv in ur bank, bud."

class economy(commands.Cog):
    def __init__(self , client) :
        self.client = client
 

    # @commands.command()
    # async def leaderboard(self,ctx,x = 1):
    #     users = await get_bank_data()
    #     leader_board = {}
    #     total = []
    #     for user in users:
    #         name = int(user)
    #         total_amount = users[user]["wallet"] + users[user]["bank"]
    #         leader_board[total_amount]
    #         total.append(total_amount)

    #     total = sorted(total,reverse=True)    

    #     em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
    #     index = 1
    #     for amt in total:
    #         id_ = leader_board[amt]
    #         member = client.get_user
    #         name = member.name
    #         em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
    #         if index == x:
    #             break
    #         else:
    #             index += 1

    #     await ctx.send(embed = em)
            
# Sends your balance
    @commands.command(aliases=["bal"])
    async def balance(self,ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data() 

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        em = discord.Embed(title = f"{ctx.author.name}'s balance",color = discord.Color.blue())
        em.add_field(name = "Wallet balance", value = wallet_amt)
        em.add_field(name = "Bank balance", value = bank_amt)
        em.add_field(name = "Total Balance", value = f"`{bank_amt + wallet_amt}`")
        await ctx.send(embed = em)



    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user) #has a cooldown
    async def beg(self,ctx):

        #same as last time!
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        #I deleted the halloween event
        list = ['money']
        reward_type = random.choice(list)
        if reward_type == "money":
            earnings = random.randint(0, 100)
            users[str(user.id)]["wallet"] += earnings

            #making sure the balance is saved
            with open("data/mainbank.json", "w") as f:
                json.dump(users, f)

            await ctx.send(f"Well you earned {earnings} coins")
            
    @beg.error
    async def beg_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title = "Slow it down C'mon!", color = ctx.author.color)
            embed.add_field(name = "Bruh", value = "Stop begging so much! It makes you look poor!")
            embed.add_field(name = "Try again in:", value = f"`{error.retry_after}`")
            await ctx.send(embed = embed)




    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self,ctx):
        await ctx.send("Great you claimed 50 coins")
        users = await get_bank_data()
        user = ctx.author
        await open_account(user)

        users[str(user.id)]["wallet"] += 50

        with open("data/mainbank.json", "w") as f:
            json.dump(users, f)

    @daily.error
    async def daily_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title = "Slow it down C'mon!", color = ctx.author.color)
            embed.add_field(name = "Bruh", value = "Stop moneying so much! It makes you look poor!")
            embed.add_field(name = "Try again in:", value = f"`{error.retry_after}`")
            await ctx.send(embed = embed)
        



    @commands.command()
    @commands.cooldown(1, 604800, commands.BucketType.user)
    async def weekly(self,ctx):
        await ctx.send("Great you claimed 100 coins")
        users = await get_bank_data()
        user = ctx.author
        await open_account(user)

        users[str(user.id)]["wallet"] += 100

        with open("data/mainbank.json", "w") as f:
            json.dump(users, f)

    @weekly.error
    async def weekly_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title = "Slow it down C'mon!", color = ctx.author.color)
            embed.add_field(name = "Bruh", value = "Stop moneying so much! It makes you look poor!")
            embed.add_field(name = "Try again in:", value = f"`{error.retry_after}`")
            await ctx.send(embed = embed)

    # Withdraw money from your bank account
    @commands.command()
    async def withdraw(self,ctx, amount = None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return
        
        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("You don't have that much money in your bank account!")
            return
        if amount<0:
            await ctx.send("Amount must be positive!")
            return
        
        await update_bank(ctx.author,amount)
        await update_bank(ctx.author,-1*amount,"bank")
        
        await ctx.send(f"{ctx.author.name} withdrew {amount} coins")

    # Deposit money from your wallet
    @commands.command()
    async def deposit(self,ctx, amount = None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return
        
        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("You don't have that much money in your wallet!")
            return
        if amount<0:
            await ctx.send("Amount must be positive!")
            return
        
        await update_bank(ctx.author,-1*amount)
        await update_bank(ctx.author,amount,"bank")
        
        await ctx.send(f"{ctx.author.name} deposited {amount} coins")

# Send another member coins
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def send(self,ctx, member:discord.Member, amount = None):
        await open_account(ctx.author)
        await open_account(member)
        if amount == None:
            await ctx.send("Please enter the amount")
            return
        
        bal = await update_bank(ctx.author)
        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("You don't have that much money in your bank account!")
            return
        if amount<0:
            await ctx.send("Amount must be positive!")
            return
        
        await update_bank(ctx.author,-1*amount,"bank")
        await update_bank(member,amount,"bank")
        
        await ctx.send(f"{ctx.author.name} gave {member} {amount} coins")

    @send.error
    async def give_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title = "Slow it down C'mon", color = ctx.author.color)
            embed.add_field(name = 'Stop giving', value = "Wanna make a company, Work With Us.'")
            embed.add_field(name = "Try again in:", value = f"`{error.retry_after}`")
            await ctx.send(embed)

    # @commands.command()
    # @commands.cooldown(1, 60, commands.BucketType.user)
    # async def rob(self,ctx, member:discord.Member):
    #     await open_account(ctx.author)
    #     await open_account(member)
        
    #     bal = await update_bank(member)

    #     if bal[0]<100:
    #         await ctx.send("It's not worth it!")
    #         return

    #     earnings = random.randrange(0, bal[0])
        
    #     await update_bank(ctx.author,earnings)
    #     await update_bank(member,-1*earnings)
        
    #     await ctx.send(f"{ctx.author.name} robbed {member} and got {earnings} coins")

# gamble (remove this command later because)
    # @commands.command() 
    # async def slots(self,ctx,amount = None):
    #     await open_account(ctx.author)
    #     if amount == None:
    #         await ctx.send("Please enter the amount")
    #         return
        
    #     bal = await update_bank(ctx.author)

    #     amount = int(amount)
    #     if amount > bal[0]:
    #         await ctx.send("You don't have that much money!")
    #         return
    #     if amount<0:
    #         await ctx.send("Amount must be positive!")
    #         return
        
    #     final = []
    #     for i in range(3):
    #         a = random.choice(["X", "O", "Q"])

    #         final.append(a)

    #     await ctx.send(str(final))

    #     if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
    #         await update_bank(ctx.author, 2*amount)
    #         await ctx.send("You won!")
    #     else: 
    #         await update_bank(ctx.author, -1*amount)
    #         await ctx.send("You lost!")

    # give someone coins
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator = True)
    async def give_coins(self,ctx, member:discord.Member, amount = None):
        await open_account(member)
        if amount == None:
            await ctx.send("Please enter the amount")
            return
        
        amount = int(amount)
        if amount<0:
            await ctx.send("Amount must be positive!")
            return
        await update_bank(member,amount,"bank")
        
        await ctx.send(f"{ctx.author.mention} gave {member} {amount} coins")
        await message.channel.send(f"{ctx.author.mention} gave {member} {amount} coins")

# remove coins from someone
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator = True)
    async def remove_coins(self,ctx, member:discord.Member, amount = None):
        await open_account(member)

        if amount == None:
            await ctx.send("Please enter the amount")
            return
        
        amount = int(amount)

        bal = await update_bank(member)

        if bal[0] < amount:
            await ctx.send(f"{ctx.author.mention} has less money than the amount you are trying to remove")
            return
        
        await update_bank(member,-1*amount)
        
        await ctx.send(f"{ctx.author.mention} removed {amount} coins from {member}")

        await message.channel.send(f"{ctx.author.mention} removed {amount} coins from {member}")

# -----------------------------------------------------------------------------------------------------------------
# open an account
async def open_account(user):

    users = await get_bank_data()

    with open("data/mainbank.json","r") as f:
        users = json.load(f)

    if str(user.id) in users:
        return False
    else: 
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 100
        users[str(user.id)]["bank"] = 0
    
    with open("data/mainbank.json", "w") as f:
        json.dump(users,f)
    return True

# get data from mainbank.json
async def get_bank_data():
    with open("data/mainbank.json","r") as f:
        users = json.load(f)  

    return users

# update the bank
async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data() 

    users[str(user.id)][mode] += change

    with open("data/mainbank.json","w") as f:
        json.dump(users,f)
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal


# ---------------------------------------------------------------------------------------------------------



# cooldown
@commands.Cog.listener()
async def on_command_error(self,ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if error.retry_after >= 60:
            cooldown = error.retry_after/60
            if cooldown == "1":
                plural = ""
            else: 
                plural = "s"
            
            em = discord.Embed(title = "Cooldown reached", description = f"This command is on cooldown, you can use it in {round (cooldown, 2)} minute{plural}",color = discord.Color.red())
        if error.retry_after >= 3600:
            cooldown = error.retry_after/3600
            if cooldown == "1":
                plural = ""
            else: 
                plural = "s"
            
            em = discord.Embed(title = "Cooldown reached", description = f"This command is on cooldown, you can use it in {round (cooldown, 2)} hour{plural}",color = discord.Color.red())
        if error.retry_after >= 86400:
            cooldown = error.retry_after/86400
            if cooldown == "1":
                plural = ""
            else: 
                plural = "s"
            
            em = discord.Embed(title = "Cooldown reached", description = f"This command is on cooldown, you can use it in {round (cooldown, 2)} day{plural}",color = discord.Color.red())
        if error.retry_after >= 604800:
            cooldown = error.retry_after/604800
            if cooldown == "1":
                plural = ""
            else: 
                plural = "s"
            em = discord.Embed(title = "Cooldown reached", description = f"This command is on cooldown, you can use it in {round (cooldown, 2)} week{plural}",color = discord.Color.red())
        if error.retry_after < 60:
            if error.retry_after == "1":
                plural = ""
            else: 
                plural = "s"
            em = discord.Embed(title = "Cooldown reached", description = f"This command is on cooldown, you can use it in {round (error.retry_after, 2)} second{plural}",color = discord.Color.red())

            await ctx.member.send(embed = em)
    
        
def setup(client):
    client.add_cog(economy(client))
    print('Economy Cog Loaded !')

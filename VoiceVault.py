import discord
from discord.ext import commands, tasks

prefix = "vv!"  # Prefixo dos comandos do bot
token = "MTExOTY3NzI5NDU4NDI2Njg5Mw.GbGf0u.MVCdSOO54DYnWoqPPbbXh212NDcxJcuBt3IaF0"  # Token do seu bot do Discord

bot = commands.Bot(command_prefix=prefix)

# Evento de inicialização do bot
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user.name}")
    verifica_tempo.start()  # Inicia a tarefa de verificação de tempo

# Tarefa para verificar e acumular o tempo em voz dos membros
@tasks.loop(minutes=60)
async def verifica_tempo():
    for guild in bot.guilds:
        for member in guild.members:
            if member.voice and member.voice.channel:
                if member.voice.self_mute or member.voice.self_deaf:
                    continue
                tempo_acumulado[member.id] = tempo_acumulado.get(member.id, 0) + 1
                await atualizar_titulos(member)

# Função para atualizar os títulos dos cargos
async def atualizar_titulos(membro):
    horas_acumuladas = tempo_acumulado.get(membro.id, 0)
    novo_titulo = min(horas_acumuladas // tempo_necessario, len(cargo_titulos) - 1)
    titulo_cargo = cargo_titulos[novo_titulo]
    for cargo in membro.roles:
        if cargo.name.startswith("Title"):
            await membro.remove_roles(cargo)
    for cargo in membro.guild.roles:
        if cargo.name == titulo_cargo:
            await membro.add_roles(cargo)

# Comando para verificar o tempo acumulado do membro
@bot.command()
async def tempo(ctx):
    horas_acumuladas = tempo_acumulado.get(ctx.author.id, 0)
    await ctx.send(f"{ctx.author.mention}, you have accumulated {horas_acumuladas} hours with your microphone and audio on.")

# Execução do bot
bot.run(token)

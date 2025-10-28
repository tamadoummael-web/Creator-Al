#!/usr/bin/python3

import time
 
t = time.localtime(time.time())
localtime = time.asctime(t)
str = "Current Time:" + time.asctime(t)
 
print(str)
   # ultimate_app.py
import os, sqlite3, torch, openai
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from diffusers import StableDiffusionPipeline, StableDiffusionInpaintPipeline
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mpy
import gradio as gr

# ---- Backend FastAPI ----
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
DB_FILE = "users.db"

# Créer la base de données
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT
)""")
conn.commit()
conn.close()

# ---- Comptes classiques ----
@app.post("/signup")
def signup(email: str = Form(...), password: str = Form(...)):
    hashed = pwd_context.hash(password)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email,password) VALUES (?,?)", (email,hashed))
        conn.commit()
    except:
        conn.close()
        return {"message":"Email déjà utilisé"}
    conn.close()
    return {"message": f"Compte créé pour {email}"}

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()
    if result and pwd_context.verify(password,result[0]):
        return {"message": f"Connecté en tant que {email}"}
    return {"message":"Email ou mot de passe incorrect"}

# ---- IA Texte / Code ----
openai.api_key = os.getenv("OPENAI_API_KEY")

def generer_code(prompt, langage="Python"):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Écris un code en {langage} pour : {prompt}",
        max_tokens=300
    )
    return response.choices[0].text.strip()

def repondre_question(question):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Répond à cette question de manière claire : {question}",
        max_tokens=200
    )
    return response.choices[0].text.strip()

# ---- IA Image / Vidéo ----
model_id = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if device=="cuda" else torch.float32)
pipe = pipe.to(device)
pipe_inpaint = StableDiffusionInpaintPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if device=="cuda" else torch.float32)
pipe_inpaint = pipe_inpaint.to(device)

def generer_image(prompt):
    return pipe(prompt).images[0]

def modifier_image(image, mask_image, prompt_mod):
    return pipe_inpaint(prompt=prompt_mod, image=image, mask_image=mask_image).images[0]

def ajouter_texte(image, texte, position=(10,10), couleur="white"):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text(position, texte, fill=couleur, font=font)
    return image

def creer_video(images, musique_path=None, fps=2):
    clips = [mpy.ImageClip(img).set_duration(1) for img in images]
    video = mpy.concatenate_videoclips(clips, method="compose")
    if musique_path:
        audio = mpy.AudioFileClip(musique_path)
        video = video.set_audio(audio)
    video.write_videofile("video_finale.mp4", fps=fps)
    return "video_finale.mp4"

# ---- Interface Gradio ----
def interface(prompt_texte="", type_code="Python", prompt_image="", texte_video="", musique_path=None, question=""):
    resultats = {}
    
    # Générer code
    if prompt_texte:
        resultats["Code généré"] = generer_code(prompt_texte, type_code)
    
    # Répondre question
    if question:
        resultats["Réponse"] = repondre_question(question)
    
    # Générer images
    images = []
    if prompt_image:
        images = [generer_image(prompt_image) for _ in range(5)]
        if texte_video:
            images = [ajouter_texte(img, texte_video) for img in images]
        video_path = creer_video(images, musique_path)
        resultats["Vidéo"] = video_path
    
    return resultats

iface = gr.Interface(
    fn=interface,
    inputs=[
        gr.Textbox(label="Prompt pour code"),
        gr.Dropdown(label="Langage du code", choices=["Python","JavaScript","Java"]),
        gr.Textbox(label="Prompt pour image"),
        gr.Textbox(label="Texte à ajouter sur la vidéo", optional=True),
        gr.Textbox(label="Chemin musique (mp3)", optional=True),
        gr.Textbox(label="Question à poser", optional=True)
    ],
    outputs="json",
    title="Ultimate IA : Questions, Code, Images, Vidéos, Comptes"
)

iface.launch() 
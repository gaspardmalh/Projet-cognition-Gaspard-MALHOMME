import pygame
import sys
import random
import time

# --- REGLAGES DU JEU ---
FONT_NAME = "timesnewroman" 
BG_COLOR = (220, 220, 220)  # Gris très clair
TEXT_COLOR = (0, 0, 0)

# 1. TEMPS
FIXATION_TIME = 1000        # La croix reste 1 seconde
STIMULUS_TIME = 1000        # Lecture : 1.2 secondes
BLANK_TIME = 800            # Pause

# 2. DIFFICULTÉ
SIZE_BASE = 70              
SIZE_DIFF = 3               # 4 pixels de différence
NB_TRIALS = 20              # 20 essais comme demandé

# Liste des paires (Appendice article)
DATA_PAIRS = [
    ("BATEAU", "TEAUBA"), ("BUREAU", "REAUBU"), ("CAMION", "MIONCA"),
    ("CANAL", "NALCA"), ("GENOU", "NOUGE"), ("JARDIN", "DINJAR"),
    ("LAPIN", "PINLA"), ("PARFUM", "FUMPAR"), ("TUYAU", "YUTAU"),
    ("CITRON", "TRONCI"),
    ("CORDON", "DONCOR"),
    ("DINDON", "DONDIN"),
    ("GUIDON", "DONGUI"),
    ("MOUTON", "TONMOU"),
    ("PANIER", "NIERPA"),
    ("PARDON", "DONPAR"),
]

class Game:
    def __init__(self):
        pygame.init()
        # Résolution confortable
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Expérience : Biais de Hauteur Lexicale")
        
        # Polices
        try:
            self.font_base = pygame.font.SysFont(FONT_NAME, SIZE_BASE)
            # On prépare les tailles
            self.font_taller = pygame.font.SysFont(FONT_NAME, SIZE_BASE + SIZE_DIFF)
            self.font_smaller = pygame.font.SysFont(FONT_NAME, SIZE_BASE - SIZE_DIFF)
            self.font_ui = pygame.font.SysFont("arial", 26)
            self.font_title = pygame.font.SysFont("arial", 36, bold=True)
            self.font_big_stat = pygame.font.SysFont("arial", 48, bold=True)
        except:
            # Fallback si police pas trouvée
            self.font_base = pygame.font.Font(None, SIZE_BASE)
            self.font_ui = pygame.font.Font(None, 26)

        self.trials = self.generate_trials()
        
        # --- NOUVELLES STATS ---
        # On compte simplement ce qui s'est passé
        self.stats = {
            "total": 0,
            "correct": 0,
            "overest_clean_word": 0,   # A choisi le mot bien écrit (alors qu'il ne l'était pas)
            "overest_bad_word": 0,     # A choisi le mot mal écrit (alors qu'il ne l'était pas)
            
            # Pour les stats avancées (Détail contextuel)
            "equal_attempts": 0,
            "equal_bias_clean": 0,     # Biais sur égalité
            "smaller_attempts": 0,
            "smaller_bias_clean": 0    # Résistance réalité (Mot petit vu grand)
        }

    def generate_trials(self):
        trials = []
        for _ in range(NB_TRIALS):
            word, pseudo = random.choice(DATA_PAIRS)
            
            # 70% de miroirs visuels (flip) pour bien voir la déformation
            distractor_type = "mirror" if random.random() < 0.7 else "syllable"
            
            # Conditions de taille (33% Equal, 33% Word+, 33% Word-)
            r = random.random()
            if r < 0.33:   size_cond = "equal"
            elif r < 0.66: size_cond = "diff_word_taller"
            else:          size_cond = "diff_word_smaller"
            
            trials.append({
                "clean_word": word,
                "bad_word_text": word if distractor_type == "mirror" else pseudo,
                "is_mirror_img": (distractor_type == "mirror"),
                "size_cond": size_cond,
                "pos_clean": random.choice(["left", "right"]) # Position du mot CORRECT
            })
        return trials
    
    def generate_trials(self):
        trials = []
        
        # --- CORRECTION : Distribution Forcée et Équilibrée ---
        # Sur 20 essais, on force : 
        # 7 cas "Egaux", 7 cas "Mot Normal +Grand", 6 cas "Mot Normal +Petit"
        nb = NB_TRIALS//3
        conditions = ["equal"] * nb + ["diff_word_taller"] * nb + ["diff_word_smaller"] * (NB_TRIALS-2*nb)
        random.shuffle(conditions) # On mélange le tout
        
        for condition in conditions:
            word, pseudo = random.choice(DATA_PAIRS)
            
            # 70% de miroirs visuels
            distractor_type = "mirror" if random.random() < 0.7 else "syllable"
            
            trials.append({
                "clean_word": word,
                "bad_word_text": word if distractor_type == "mirror" else pseudo,
                "is_mirror_img": (distractor_type == "mirror"),
                "size_cond": condition, # On utilise la condition piochée dans la liste équilibrée
                "pos_clean": random.choice(["left", "right"])
            })
        return trials

    def draw_stimulus(self, text, x, y, font, do_flip):
        surface = font.render(text, True, TEXT_COLOR)
        if do_flip:
            surface = pygame.transform.flip(surface, True, False)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def run_trial(self, trial):
        # 1. Fixation
        self.screen.fill(BG_COLOR)
        # Belle croix de fixation
        pygame.draw.circle(self.screen, (200, 50, 50), (640, 360), 8)
        pygame.display.flip()
        pygame.time.wait(FIXATION_TIME)

        # 2. Choix des tailles
        font_clean = self.font_base
        font_bad = self.font_base

        if trial["size_cond"] == "diff_word_taller":
            font_clean = self.font_taller
            font_bad = self.font_smaller
        elif trial["size_cond"] == "diff_word_smaller":
            font_clean = self.font_smaller
            font_bad = self.font_taller
        # Sinon equal : restent base

        # 3. Affichage
        self.screen.fill(BG_COLOR)
        offset = 280 # Ecartement
        y_pos = 360

        # Logique d'affichage selon la position du mot propre
        if trial["pos_clean"] == "left":
            # Mot propre à GAUCHE
            self.draw_stimulus(trial["clean_word"], 640 - offset, y_pos, font_clean, False)
            # Mot sale à DROITE
            self.draw_stimulus(trial["bad_word_text"], 640 + offset, y_pos, font_bad, trial["is_mirror_img"])
        else:
            # Mot sale à GAUCHE
            self.draw_stimulus(trial["bad_word_text"], 640 - offset, y_pos, font_bad, trial["is_mirror_img"])
            # Mot propre à DROITE
            self.draw_stimulus(trial["clean_word"], 640 + offset, y_pos, font_clean, False)

        pygame.display.flip()
        time.sleep(STIMULUS_TIME / 1000.0)
        
        # 4. Masque
        self.screen.fill(BG_COLOR)
        pygame.display.flip()

        # 5. Attente Réponse
        response = None
        while response is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: response = "left"
                    elif event.key == pygame.K_RIGHT: response = "right"
                    elif event.key == pygame.K_DOWN: response = "equal"
                    elif event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
        
        self.process_response(trial, response)
        pygame.time.wait(BLANK_TIME)

    def run_trial(self, trial):
        # 1. Fixation (Gros point rouge)
        self.screen.fill(BG_COLOR)
        pygame.draw.circle(self.screen, (200, 50, 50), (640, 360), 8)
        pygame.display.flip()
        pygame.time.wait(FIXATION_TIME)

        # 2. Préparation
        font_clean = self.font_base
        font_bad = self.font_base
        if trial["size_cond"] == "diff_word_taller":
            font_clean = self.font_taller
            font_bad = self.font_smaller
        elif trial["size_cond"] == "diff_word_smaller":
            font_clean = self.font_smaller
            font_bad = self.font_taller

        # 3. Affichage (Mots + Point central maintenu)
        self.screen.fill(BG_COLOR)
        
        # --- MODIFICATION ICI : On garde le point rouge ---
        # On le fait un tout petit peu plus petit (6px au lieu de 8px) 
        # pour donner une sensation de "focus"
        pygame.draw.circle(self.screen, (200, 50, 50), (640, 360), 6)
        
        offset = 280
        y_pos = 360

        if trial["pos_clean"] == "left":
            self.draw_stimulus(trial["clean_word"], 640 - offset, y_pos, font_clean, False)
            self.draw_stimulus(trial["bad_word_text"], 640 + offset, y_pos, font_bad, trial["is_mirror_img"])
        else:
            self.draw_stimulus(trial["bad_word_text"], 640 - offset, y_pos, font_bad, trial["is_mirror_img"])
            self.draw_stimulus(trial["clean_word"], 640 + offset, y_pos, font_clean, False)

        pygame.display.flip()
        time.sleep(STIMULUS_TIME / 1000.0)
        
        # 4. Masque
        self.screen.fill(BG_COLOR)
        pygame.display.flip()

        # 5. Réponse
        response = None
        while response is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: response = "left"
                    elif event.key == pygame.K_RIGHT: response = "right"
                    elif event.key == pygame.K_DOWN: response = "equal"
                    elif event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
        
        self.process_response(trial, response)
        pygame.time.wait(BLANK_TIME)

    def process_response(self, trial, response):
        self.stats["total"] += 1
        
        # --- 0. Initialisation sécurisée des nouveaux compteurs (si pas dans __init__) ---
        # On s'assure que les clés existent pour éviter les erreurs
        keys_to_check = ["underest_clean_word", "underest_bad_word", "overest_clean_word", "overest_bad_word"]
        for k in keys_to_check:
            if k not in self.stats:
                self.stats[k] = 0

        # --- 1. Déterminer la Vérité Terrain ---
        actual_tallest = "equal"
        if trial["size_cond"] == "diff_word_taller":
            actual_tallest = trial["pos_clean"]
        elif trial["size_cond"] == "diff_word_smaller":
            actual_tallest = "right" if trial["pos_clean"] == "left" else "left"

        # --- 2. Vérifier si Correct ---
        if response == actual_tallest:
            self.stats["correct"] += 1
            # Si c'est juste, on n'augmente aucun compteur d'erreur
            return 

        # --- 3. Analyse de l'Erreur (Logique Double Compteur) ---
        # On identifie ce que le joueur a CHOISI vs la RÉALITÉ
        
        user_chose_clean = (response == trial["pos_clean"])
        
        pos_bad = "right" if trial["pos_clean"] == "left" else "left"
        user_chose_bad = (response == pos_bad)
        
        user_chose_equal = (response == "equal")

        # CAS A : Joueur choisit le MOT NORMAL (mais c'est faux)
        # Il a vu le mot normal plus grand que la réalité (Surestimation Normal)
        # ET il a vu le mot bizarre plus petit que la réalité (Sous-estimation Bizarre)
        if user_chose_clean:
            self.stats["overest_clean_word"] += 1
            self.stats["underest_bad_word"] += 1

        # CAS B : Joueur choisit le MOT BIZARRE (mais c'est faux)
        # Il a vu le bizarre plus grand (Surestimation Bizarre)
        # ET il a vu le normal plus petit (Sous-estimation Normal)
        elif user_chose_bad:
            self.stats["overest_bad_word"] += 1
            self.stats["underest_clean_word"] += 1

        # CAS C : Joueur choisit ÉGAL (mais c'est faux)
        elif user_chose_equal:
            # Sous-cas C1 : En réalité, le Mot Normal était le plus grand
            # Le joueur l'a "rabaissé" (Sous-estimation Normal)
            # Et il a "rehaussé" le mot bizarre (Surestimation Bizarre)
            if trial["size_cond"] == "diff_word_taller":
                self.stats["underest_clean_word"] += 1
                self.stats["overest_bad_word"] += 1
            
            # Sous-cas C2 : En réalité, le Mot Bizarre était le plus grand
            # Le joueur a "rehaussé" le mot normal (Surestimation Normal)
            # Et il a "rabaissé" le mot bizarre (Sous-estimation Bizarre)
            elif trial["size_cond"] == "diff_word_smaller":
                self.stats["overest_clean_word"] += 1
                self.stats["underest_bad_word"] += 1

        # --- 4. Stats Avancées (Conservation de l'existant) ---
        # On garde ces compteurs pour tes affichages détaillés "D"
        if trial["size_cond"] == "equal": 
            self.stats["equal_attempts"] += 1
            # Si c'était égal et qu'on a choisi le mot normal, c'est le biais pur
            if user_chose_clean: self.stats["equal_bias_clean"] += 1
            
        if trial["size_cond"] == "diff_word_smaller": 
            self.stats["smaller_attempts"] += 1
            # Résistance à la réalité : le mot était petit, mais on l'a vu grand (clean) ou égal
            # (Note : selon ta nouvelle logique, "égal" ici compte aussi comme surestimation du clean, donc c'est cohérent)
            if user_chose_clean or user_chose_equal: 
                self.stats["smaller_bias_clean"] += 1


    def draw_text_centered(self, lines, y_start, default_col=(0,0,0)):
        y = y_start
        for line in lines:
            font = self.font_ui
            col = default_col
            
            # Gestion basique des styles via préfixes
            if line.startswith("TITLE:"):
                font = self.font_title
                line = line.replace("TITLE:", "")
            elif line.startswith("BIG:"):
                font = self.font_big_stat
                line = line.replace("BIG:", "")
                col = (0, 0, 150) # Bleu
            
            # Couleurs sémantiques
            if "Mot Correct" in line: col = (0, 100, 0)
            if "Mot Déformé" in line: col = (150, 0, 0)
            
            txt = font.render(line, True, col)
            rect = txt.get_rect(center=(640, y))
            self.screen.blit(txt, rect)
            y += 40
            if line == "": y -= 20

    def show_results(self):
        show_advanced = False
        
        while True:
            self.screen.fill(BG_COLOR)
            
            # Calculs
            total = self.stats["total"]
            if total == 0: total = 1 # Eviter div/0
            
            pct_correct = (self.stats["correct"] / total) * 100
            pct_bias_clean = (self.stats["overest_clean_word"] / total) * 100
            pct_bias_bad = (self.stats["overest_bad_word"] / total) * 100
            
            # --- ECRAN PRINCIPAL ---
            if not show_advanced:
                lines = [
                    "TITLE:RÉSULTATS DE L'EXPÉRIENCE",
                    "",
                    f"Estimation Correcte : {pct_correct:.1f} %",
                    "",
                    "Statistiques de sur-estimation:",
                    "",
                    f"BIG:{pct_bias_clean:.1f} %",
                    "Sur-estimation du Mot Normalement écrit",
                    "(Vous l'avez vu plus grand qu'il ne l'était)",
                    "",
                    f"BIG:{pct_bias_bad:.1f} %",
                    "Sur-estimation du Mot Déformé",
                    "(Vous l'avez vu plus grand qu'il ne l'était)",
                    "",
                    "-------------------------------",
                    "Appuyez sur [ESPACE] pour Quitter"
                ]
                self.draw_text_centered(lines, 100)
            
            # --- ECRAN AVANCÉ ---
            else:
                show_advanced=False

            pygame.display.flip()

            # Gestion clavier boucle
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.quit(); sys.exit()
                    if event.key == pygame.K_d:
                        show_advanced = not show_advanced

    def run(self):
        intro = [
            "TITLE:JEU DE PERCEPTION",
            "",
            "Comparez la hauteur verticale des deux mots, en fixant le point rouge.",
            f"Il y a {NB_TRIALS} tours.",
            "",
            "Répondre avec les flèches pour indiquer quel mot est le plus grand :",
            "[ GAUCHE ]    [ BAS (Égal) ]    [ DROITE ]",
            "",
            "",
            "[ Appuyez sur une touche ]"
        ]
        self.screen.fill(BG_COLOR)
        self.draw_text_centered(intro, 150)
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: waiting = False
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        for trial in self.trials:
            self.run_trial(trial)
            
        self.show_results()

if __name__ == "__main__":
    game = Game()
    game.run()
import pygame
from code.Const import *
from code.DBProxy import DBProxy


class Score:
    def __init__(self, screen, score, result):
        self.screen = screen
        self.score  = score
        self.result = result
        self.name   = ""
        self.state  = "input"   # "input" | "board"
        self.board  = []
        self.db     = DBProxy()

        self._fb  = pygame.font.SysFont("monospace", 34, bold=True)
        self._fm  = pygame.font.SysFont("monospace", 20)
        self._fs  = pygame.font.SysFont("monospace", 14)

    # ------------------------------------------------------------------
    def handle(self, event):
        if event.type != pygame.KEYDOWN:
            return None

        if self.state == "input":
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == pygame.K_RETURN and self.name:
                self.db.save(self.name, self.score)
                self.board = self.db.top()
                self.db.close()
                self.state = "board"
            elif len(self.name) < 4 and event.unicode.isalnum():
                self.name += event.unicode.upper()

        elif self.state == "board":
            if event.key == pygame.K_RETURN:
                return "menu"

        return None

    # ------------------------------------------------------------------
    def draw(self):
        self.screen.fill(DARK_BG)

        result_txt   = "VITÓRIA!" if self.result == "win" else "GAME OVER"
        result_color = CYAN       if self.result == "win" else RED
        t = self._fb.render(result_txt, True, result_color)
        self.screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 28))

        sc = self._fm.render(f"PONTUAÇÃO: {self.score}", True, WHITE)
        self.screen.blit(sc, (WIDTH // 2 - sc.get_width() // 2, 74))

        if self.state == "input":
            self._draw_input()
        else:
            self._draw_board()

    def _draw_input(self):
        p = self._fm.render("Digite seu nome (até 4 letras):", True, PURPLE)
        self.screen.blit(p, (WIDTH // 2 - p.get_width() // 2, 130))

        cursor = self._fb.render(self.name + "_", True, CYAN)
        self.screen.blit(cursor, (WIDTH // 2 - cursor.get_width() // 2, 162))

        h = self._fs.render("ENTER para confirmar", True, (90, 90, 140))
        self.screen.blit(h, (WIDTH // 2 - h.get_width() // 2, 210))

    def _draw_board(self):
        hdr = self._fm.render("— TOP 10 —", True, PURPLE)
        self.screen.blit(hdr, (WIDTH // 2 - hdr.get_width() // 2, 128))

        for i, (nm, sc, ts) in enumerate(self.board[:10]):
            color = CYAN if nm == self.name else WHITE
            line  = self._fs.render(f"{i+1:2}. {nm:<4}  {sc:>6}  {ts}", True, color)
            self.screen.blit(line, (WIDTH // 2 - line.get_width() // 2,
                                    154 + i * 22))

        hint = self._fs.render("ENTER — voltar ao menu", True, (70, 70, 110))
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 26))

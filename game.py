class Game:
    WALL = '#'
    EMPTY = '.'
    TARGET = '@'

    def __init__(self, grid):
        self._grid = [list(row) for row in grid]
        self._balls = self._find_balls()
        self._targets = self._find_targets()
        self._selected_ball = None

    @property
    def grid(self):
        return self._grid

    @property
    def balls(self):
        return self._balls

    @property
    def targets(self):
        return self._targets

    @property
    def selected_ball(self):
        return self._selected_ball

    @selected_ball.setter
    def selected_ball(self, value):
        self._selected_ball = value

    @property
    def rows(self):
        return len(self._grid)

    @property
    def cols(self):
        return len(self._grid[0]) if self._grid else 0

    def _find_balls(self):
        return [{'pos': (r, c), 'color': ch}
                for r, row in enumerate(self._grid)
                for c, ch in enumerate(row) if ch.islower()]

    def _find_targets(self):
        return [{'pos': (r, c), 'color': ch.lower()}
                for r, row in enumerate(self._grid)
                for c, ch in enumerate(row) if ch.isupper()]

    @staticmethod
    def get_direction(from_pos, to_pos):
        dr = to_pos[0] - from_pos[0]
        dc = to_pos[1] - from_pos[1]
        if abs(dr) > abs(dc):
            return (1 if dr > 0 else -1, 0)
        else:
            return (0, 1 if dc > 0 else -1)

    def select_ball(self, row, col):
        if self.get_cell(row, col).islower():
            self.selected_ball = (row, col)
            return True
        return False

    def move_selected(self, target_row, target_col):
        if not self.selected_ball:
            return False

        from_row, from_col = self.selected_ball
        ball = next((b for b in self.balls if b['pos'] == (from_row, from_col)), None)
        if not ball:
            return False

        dr, dc = self.get_direction((from_row, from_col), (target_row, target_col))
        color = ball['color']
        self._grid[from_row][from_col] = self.EMPTY

        r, c = from_row, from_col
        while True:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < self.rows and 0 <= nc < self.cols):
                break

            cell = self._grid[nr][nc]
            if cell == self.WALL or (cell.islower() and (nr, nc) != (from_row, from_col)):
                break
            if cell.isupper() and cell.lower() != color:
                break
            if cell.isupper() and cell.lower() == color:
                self._grid[nr][nc] = self.TARGET
                self._balls.remove(ball)
                self.selected_ball = None
                return True

            r, c = nr, nc

        self._grid[r][c] = color
        ball['pos'] = (r, c)
        self.selected_ball = None
        return True

    def get_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self._grid[row][col]
        return None

    def check_win(self):
        return len(self.balls) == 0

    @classmethod
    def load_level(cls, filename):
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        return cls(lines)

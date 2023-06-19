class Level:
    def __init__(self, chase_duration, scatter_duration, fright_duration, elroy_1_dots, elroy_1_speed, elroy_2_dots,
                 elroy_2_speed, pacman_speed_normal, pacman_dots_normal, pacman_speed_fright, pacman_dots_fright,
                 ghost_speed_normal, ghost_speed_fright, ghost_speed_tunnel, clyde_dots_to_leave,
                 inky_dots_to_leave, bonus, bonus_points):
        self.chase_duration = chase_duration
        self.scatter_duration = scatter_duration
        self.fright_duration = fright_duration
        self.elroy_1_dots = elroy_1_dots
        self.elroy_1_speed = elroy_1_speed
        self.elroy_2_dots = elroy_2_dots
        self.elroy_2_speed = elroy_2_speed
        self.pacman_speed_normal = pacman_speed_normal
        self.pacman_dots_normal = pacman_dots_normal
        self.pacman_speed_fright = pacman_speed_fright
        self.pacman_dots_fright = pacman_dots_fright
        self.ghost_speed_normal = ghost_speed_normal
        self.ghost_speed_fright = ghost_speed_fright
        self.ghost_speed_tunnel = ghost_speed_tunnel
        self.clyde_dots_to_leave = clyde_dots_to_leave
        self.inky_dots_to_leave = inky_dots_to_leave
        self.bonus = bonus
        self.bonus_points = bonus_points

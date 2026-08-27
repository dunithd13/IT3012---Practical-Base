from agent import SearchAgent
import random
import tkinter as tk


class VisualGridHuntGame:
    """
    Pacman-style grid environment for IT3012 Intelligent Agents.

    The environment provides:
    - Agent position
    - Walls
    - Food
    - Opponents
    - Toxic traps
    - Score
    - Global information required by SearchAgent
    """

    def __init__(
        self,
        width=10,
        height=10,
        num_food=10,
        num_opponents=2,
        custom_walls=None
    ):

        self.width = width
        self.height = height

        # Agent starts at bottom-left
        self.agent_pos = [0, 0]

        # ==================================================
        # WALLS
        # ==================================================

        if custom_walls is not None:
            self.walls = set(custom_walls)
        else:
            self.walls = {
                (2, 2),
                (2, 3),
                (5, 5),
                (6, 5),
                (3, 7)
            }

        # ==================================================
        # FOOD
        # ==================================================

        self.food_positions = set()

        while len(self.food_positions) < num_food:

            fx = random.randint(0, self.width - 1)
            fy = random.randint(0, self.height - 1)

            pos_tuple = (fx, fy)

            if (
                pos_tuple != (0, 0)
                and pos_tuple not in self.walls
            ):
                self.food_positions.add(pos_tuple)

        # ==================================================
        # OPPONENTS
        # ==================================================

        self.opponents = []

        while len(self.opponents) < num_opponents:

            ox = random.randint(0, self.width - 1)
            oy = random.randint(0, self.height - 1)

            op_pos = [ox, oy]

            if (
                tuple(op_pos) != (0, 0)
                and tuple(op_pos) not in self.walls
                and tuple(op_pos) not in self.food_positions
            ):
                self.opponents.append(op_pos)

        # ==================================================
        # TOXIC TRAPS
        # ==================================================

        self.toxic_traps = set()

        desired_traps = max(3, self.width // 2)

        while len(self.toxic_traps) < desired_traps:

            tx = random.randint(0, self.width - 1)
            ty = random.randint(0, self.height - 1)

            pos_tuple = (tx, ty)

            if (
                pos_tuple != (0, 0)
                and pos_tuple not in self.walls
                and pos_tuple not in self.food_positions
                and pos_tuple not in {
                    tuple(op) for op in self.opponents
                }
            ):
                self.toxic_traps.add(pos_tuple)

        # ==================================================
        # GAME STATE
        # ==================================================

        self.score = 0
        self.steps = 0
        self.collision = False

    # ======================================================
    # PERCEPT
    # ======================================================

    def get_percept(self):

        x, y = self.agent_pos

        # Check wall directly above the agent
        wall_ahead = False

        if y + 1 >= self.height:
            wall_ahead = True

        elif (x, y + 1) in self.walls:
            wall_ahead = True

        # Is food at current position?
        food_here = (
            tuple(self.agent_pos)
            in self.food_positions
        )

        return {

            # Current position
            "agent_pos": list(self.agent_pos),

            # Simple-reflex information
            "wall_ahead": wall_ahead,
            "food_here": food_here,

            # ==================================================
            # SEARCH INFORMATION
            # ==================================================

            "grid_size": (
                self.width,
                self.height
            ),

            "walls": list(self.walls),

            "all_food": list(
                self.food_positions
            ),

            # ==================================================
            # OTHER ENVIRONMENT INFORMATION
            # ==================================================

            "opponent_positions": [
                list(op)
                for op in self.opponents
            ],

            "smells_toxin": (
                tuple(self.agent_pos)
                in self.toxic_traps
            ),

            "score": self.score,

            "remaining_food": len(
                self.food_positions
            ),

            "collision": self.collision
        }

 

    def execute_action(self, action: str):

        self.steps += 1

        new_pos = list(self.agent_pos)


        if action == "Up":

            new_pos[1] = min(
                self.height - 1,
                new_pos[1] + 1
            )

        elif action == "Down":

            new_pos[1] = max(
                0,
                new_pos[1] - 1
            )

        elif action == "Left":

            new_pos[0] = max(
                0,
                new_pos[0] - 1
            )

        elif action == "Right":

            new_pos[0] = min(
                self.width - 1,
                new_pos[0] + 1
            )

        elif action == "Stay":

            pass



        if tuple(new_pos) in self.walls:

            self.score -= 5

        else:

            self.agent_pos = new_pos



        tuple_pos = tuple(self.agent_pos)

        if tuple_pos in self.food_positions:

            self.food_positions.remove(
                tuple_pos
            )

            self.score += 20



        if tuple_pos in self.toxic_traps:

            self.score -= 15



        for op in self.opponents:

            move = random.choice(
                [
                    "Up",
                    "Down",
                    "Left",
                    "Right",
                    "Stay"
                ]
            )

            if (
                move == "Up"
                and op[1] < self.height - 1
            ):
                op[1] += 1

            elif (
                move == "Down"
                and op[1] > 0
            ):
                op[1] -= 1

            elif (
                move == "Left"
                and op[0] > 0
            ):
                op[0] -= 1

            elif (
                move == "Right"
                and op[0] < self.width - 1
            ):
                op[0] += 1

            # Collision with opponent
            if op == self.agent_pos:

                self.score -= 50
                self.collision = True

  

    def is_done(self):

        return (
            len(self.food_positions) == 0
            or self.steps >= 60
            or self.collision
        )




class GridGameGUI:
    """
    Tkinter GUI for the grid environment.

    SearchAgent is responsible for selecting the action.
    """

    def __init__(
        self,
        root,
        width=10,
        height=10,
        num_food=12,
        num_opponents=2,
        walls=None
    ):

        self.root = root

        self.root.title(
            "IT3012 - Search Agent Grid Hunt"
        )

      

        self.env = VisualGridHuntGame(
            width=width,
            height=height,
            num_food=num_food,
            num_opponents=num_opponents,
            custom_walls=walls
        )

       

        self.agent = SearchAgent()

        
        

        self.agent.active_algo = "A*"

        

        max_canvas_dim = 600

        self.cell_size = max(
            20,
            min(
                max_canvas_dim // self.env.width,
                max_canvas_dim // self.env.height
            )
        )

        canvas_w = (
            self.env.width
            * self.cell_size
        )

        canvas_h = (
            self.env.height
            * self.cell_size
        )

        self.canvas = tk.Canvas(
            root,
            width=canvas_w,
            height=canvas_h,
            bg="white"
        )

        self.canvas.pack()

        

        self.label = tk.Label(
            root,
            text="Algorithm: A* | Score: 0 | Steps: 0",
            font=("Arial", 14)
        )

        self.label.pack(pady=10)


        self.btn = tk.Button(
            root,
            text="Start Simulation",
            command=self.run_loop,
            font=("Arial", 12),
            bg="#000066",
            fg="white"
        )

        self.btn.pack(pady=5)

        # Draw initial grid
        self.draw_grid()

    

    def draw_grid(self):

        self.canvas.delete("all")

        

        for x in range(self.env.width):

            for y in range(self.env.height):

                x1 = (
                    x
                    * self.cell_size
                )

                y1 = (
                    self.env.height
                    - 1
                    - y
                ) * self.cell_size

                x2 = (
                    x1
                    + self.cell_size
                )

                y2 = (
                    y1
                    + self.cell_size
                )

                # Wall / normal cell
                if (x, y) in self.env.walls:

                    color = "#64748b"

                else:

                    color = "#f1f5f9"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="#cbd5e1"
                )

                # Wall label
                if (
                    self.cell_size >= 40
                    and (x, y) in self.env.walls
                ):

                    self.canvas.create_text(
                        x1
                        + self.cell_size / 2,

                        y1
                        + self.cell_size / 2,

                        text="W",

                        fill="white",

                        font=(
                            "Arial",
                            8,
                            "bold"
                        )
                    )


        for fx, fy in self.env.food_positions:

            offset = (
                self.cell_size
                * 0.25
            )

            x1 = (
                fx
                * self.cell_size
                + offset
            )

            y1 = (
                self.env.height
                - 1
                - fy
            ) * self.cell_size + offset

            self.canvas.create_oval(
                x1,
                y1,

                x1
                + self.cell_size * 0.5,

                y1
                + self.cell_size * 0.5,

                fill="#f59e0b",

                outline="#d97706"
            )


        for ox, oy in self.env.opponents:

            offset = (
                self.cell_size
                * 0.2
            )

            x1 = (
                ox
                * self.cell_size
                + offset
            )

            y1 = (
                self.env.height
                - 1
                - oy
            ) * self.cell_size + offset

            self.canvas.create_rectangle(
                x1,
                y1,

                x1
                + self.cell_size * 0.6,

                y1
                + self.cell_size * 0.6,

                fill="#990000",

                outline="#7a0000"
            )

        # ==================================================
        # TOXIC TRAPS
        # ==================================================

        for tx, ty in self.env.toxic_traps:

            offset = (
                self.cell_size
                * 0.2
            )

            x1 = (
                tx
                * self.cell_size
                + offset
            )

            y1 = (
                self.env.height
                - 1
                - ty
            ) * self.cell_size + offset

            x2 = (
                x1
                + self.cell_size * 0.6
            )

            y2 = (
                y1
                + self.cell_size * 0.6
            )

            self.canvas.create_oval(
                x1,
                y1,
                x2,
                y2,

                fill="#8b5cf6",

                outline="#6d28d9"
            )

        # ==================================================
        # AGENT
        # ==================================================

        ax, ay = self.env.agent_pos

        offset = (
            self.cell_size
            * 0.15
        )

        x1 = (
            ax
            * self.cell_size
            + offset
        )

        y1 = (
            self.env.height
            - 1
            - ay
        ) * self.cell_size + offset

        self.canvas.create_oval(
            x1,
            y1,

            x1
            + self.cell_size * 0.7,

            y1
            + self.cell_size * 0.7,

            fill="#000066",

            outline="#1e3a8a"
        )

    # ======================================================
    # RUN SIMULATION
    # ======================================================

    def run_loop(self):

        self.btn.config(
            state="disabled"
        )

        def step():

            if not self.env.is_done():

                # ==================================================
                # GET PERCEPT
                # ==================================================

                percept = (
                    self.env.get_percept()
                )

                # ==================================================
                # ASK SEARCH AGENT FOR ACTION
                # ==================================================

                action = (
                    self.agent.sense_and_act(
                        percept
                    )
                )

                # ==================================================
                # EXECUTE ACTION
                # ==================================================

                self.env.execute_action(
                    action
                )

                # ==================================================
                # REDRAW
                # ==================================================

                self.draw_grid()

                # ==================================================
                # UPDATE INFORMATION
                # ==================================================

                self.label.config(
                    text=(
                        f"Algorithm: "
                        f"{self.agent.active_algo}"
                        f" | Score: "
                        f"{self.env.score}"
                        f" | Steps: "
                        f"{self.env.steps}"
                        f" | Action: "
                        f"{action}"
                    )
                )

                # Continue after 250 ms
                self.root.after(
                    250,
                    step
                )

            else:

                # ==================================================
                # GAME OVER
                # ==================================================

                if self.env.collision:

                    end_text = (
                        "Collision! "
                        "Game Over! "
                        f"Final Score: "
                        f"{self.env.score}"
                    )

                elif len(self.env.food_positions) == 0:

                    end_text = (
                        "All Food Collected! "
                        f"Final Score: "
                        f"{self.env.score}"
                    )

                else:

                    end_text = (
                        "Finished! "
                        f"Final Score: "
                        f"{self.env.score}"
                    )

                self.label.config(
                    text=end_text
                )

                self.btn.config(
                    state="normal"
                )

        # Start simulation
        step()


# ==========================================================
# MAIN PROGRAM
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = GridGameGUI(
        root,

        width=12,
        height=12,

        num_food=15,

        num_opponents=0
    )

    root.mainloop()
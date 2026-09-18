import random
import math
from collections import deque
import heapq

from logic_engine import KnowledgeBase


# ==========================================================
# SIMPLE REFLEX AGENT
# ==========================================================

class SimpleReflexAgent:

    def sense_and_act(self, percept):

        if percept["food_here"]:
            return "Stay"

        if percept["wall_ahead"]:
            return "Left"

        return "Up"


# ==========================================================
# MODEL-BASED AGENT
# ==========================================================

class ModelBasedAgent:

    def __init__(self):

        self.last_action = None
        self.stuck_counter = 0


    def sense_and_act(self, percept):

        if percept["food_here"]:
            return "Stay"

        if percept["wall_ahead"]:

            if self.last_action == "Left":
                action = "Right"
            else:
                action = "Left"

            self.last_action = action

            return action

        self.last_action = "Up"

        return "Up"


# ==========================================================
# SEARCH AGENT
# ==========================================================

class SearchAgent:

    def __init__(self):

        # --------------------------------------------------
        # DEFAULT ALGORITHM
        # --------------------------------------------------

        self.active_algo = "ASTAR"

        # --------------------------------------------------
        # CURRENT PLAN
        # --------------------------------------------------

        self.current_plan = []

        # ==================================================
        # LAB 05 - KNOWLEDGE BASE
        # ==================================================

        self.kb = KnowledgeBase()

        # --------------------------------------------------
        # RULE 1
        #
        # TargetVisible AND HasDust
        #          ->
        # SafeToEngage
        # --------------------------------------------------

        self.kb.tell_rule(
            ["TargetVisible", "HasDust"],
            "SafeToEngage"
        )

        # --------------------------------------------------
        # RULE 2
        #
        # SafeToEngage AND BloodseekerMissing
        #          ->
        # Retreat
        # --------------------------------------------------

        self.kb.tell_rule(
            ["SafeToEngage", "BloodseekerMissing"],
            "Retreat"
        )


    # ======================================================
    # BFS SEARCH
    # ======================================================

    def bfs_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):

        queue = deque()

        queue.append(
            (start_pos, [])
        )

        reached = {
            start_pos
        }

        while queue:

            current_pos, path = queue.popleft()

            # --------------------------------------------------
            # Goal Test
            # --------------------------------------------------

            if current_pos == goal_pos:
                return path

            x, y = current_pos

            neighbours = [

                ((x, y + 1), "Up"),

                ((x, y - 1), "Down"),

                ((x - 1, y), "Left"),

                ((x + 1, y), "Right")

            ]

            for next_pos, action in neighbours:

                nx, ny = next_pos

                # --------------------------------------------------
                # Boundary Check
                # --------------------------------------------------

                if nx < 0 or nx >= grid_size[0]:
                    continue

                if ny < 0 or ny >= grid_size[1]:
                    continue

                # --------------------------------------------------
                # Wall Check
                # --------------------------------------------------

                if next_pos in walls:
                    continue

                # --------------------------------------------------
                # Already Visited
                # --------------------------------------------------

                if next_pos in reached:
                    continue

                reached.add(next_pos)

                new_path = path + [action]

                queue.append(
                    (next_pos, new_path)
                )

        return None


    # ======================================================
    # DFS SEARCH
    # ======================================================

    def dfs_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):

        stack = []

        stack.append(
            (start_pos, [])
        )

        reached = {
            start_pos
        }

        while stack:

            current_pos, path = stack.pop()

            # --------------------------------------------------
            # Goal Test
            # --------------------------------------------------

            if current_pos == goal_pos:
                return path

            x, y = current_pos

            neighbours = [

                ((x, y + 1), "Up"),

                ((x, y - 1), "Down"),

                ((x - 1, y), "Left"),

                ((x + 1, y), "Right")

            ]

            for next_pos, action in neighbours:

                nx, ny = next_pos

                # --------------------------------------------------
                # Boundary Check
                # --------------------------------------------------

                if nx < 0 or nx >= grid_size[0]:
                    continue

                if ny < 0 or ny >= grid_size[1]:
                    continue

                # --------------------------------------------------
                # Wall Check
                # --------------------------------------------------

                if next_pos in walls:
                    continue

                # --------------------------------------------------
                # Already Visited
                # --------------------------------------------------

                if next_pos in reached:
                    continue

                reached.add(next_pos)

                new_path = path + [action]

                stack.append(
                    (next_pos, new_path)
                )

        return None


    # ======================================================
    # UCS SEARCH
    # ======================================================

    def ucs_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):

        frontier = []

        heapq.heappush(
            frontier,
            (
                0,
                start_pos,
                []
            )
        )

        reached = {
            start_pos: 0
        }

        while frontier:

            cost, current_pos, path = heapq.heappop(
                frontier
            )

            # --------------------------------------------------
            # Goal Test
            # --------------------------------------------------

            if current_pos == goal_pos:
                return path

            x, y = current_pos

            neighbours = [

                ((x, y + 1), "Up"),

                ((x, y - 1), "Down"),

                ((x - 1, y), "Left"),

                ((x + 1, y), "Right")

            ]

            for next_pos, action in neighbours:

                nx, ny = next_pos

                # --------------------------------------------------
                # Boundary Check
                # --------------------------------------------------

                if nx < 0 or nx >= grid_size[0]:
                    continue

                if ny < 0 or ny >= grid_size[1]:
                    continue

                # --------------------------------------------------
                # Wall Check
                # --------------------------------------------------

                if next_pos in walls:
                    continue

                # Every movement costs 1
                new_cost = cost + 1

                # --------------------------------------------------
                # First Visit OR Cheaper Path
                # --------------------------------------------------

                if (
                    next_pos not in reached
                    or new_cost < reached[next_pos]
                ):

                    reached[next_pos] = new_cost

                    new_path = path + [action]

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            next_pos,
                            new_path
                        )
                    )

        return None


    # ======================================================
    # MANHATTAN DISTANCE
    # ======================================================

    def manhattan_distance(
        self,
        pos1,
        pos2
    ):

        return (
            abs(pos1[0] - pos2[0])
            +
            abs(pos1[1] - pos2[1])
        )


    # ======================================================
    # EUCLIDEAN DISTANCE
    # ======================================================

    def euclidean_distance(
        self,
        pos1,
        pos2
    ):

        return math.sqrt(
            (pos1[0] - pos2[0]) ** 2
            +
            (pos1[1] - pos2[1]) ** 2
        )


    # ======================================================
    # LAB 05
    # TILE LOGICAL FEASIBILITY CHECK
    # ======================================================

    def is_tile_feasible(
        self,
        tile,
        food_positions,
        opponent_positions,
        toxic_traps
    ):

        """
        Determine whether a candidate tile is logically
        feasible using the Knowledge Base.

        Physical reachability is handled separately by A*.

        A tile becomes logically infeasible when the KB
        derives the fact:

            Retreat
        """

        # --------------------------------------------------
        # Clear facts from previous candidate tile
        # --------------------------------------------------

        self.kb.clear_facts()

        # ==================================================
        # CURRENT TILE PERCEPTS
        # ==================================================

        # --------------------------------------------------
        # FACT 1
        #
        # Food represents the target.
        #
        # TargetVisible
        # --------------------------------------------------

        if tile in food_positions:

            self.kb.tell_fact(
                "TargetVisible"
            )

        # --------------------------------------------------
        # FACT 2
        #
        # Toxic trap represents the dust condition.
        #
        # HasDust
        # --------------------------------------------------

        if tile in toxic_traps:

            self.kb.tell_fact(
                "HasDust"
            )

        # --------------------------------------------------
        # FACT 3
        #
        # No visible opponents means:
        #
        # BloodseekerMissing
        # --------------------------------------------------

        if len(opponent_positions) == 0:

            self.kb.tell_fact(
                "BloodseekerMissing"
            )

        # ==================================================
        # FORWARD CHAINING
        # ==================================================

        self.kb.forward_chain()

        # ==================================================
        # FEASIBILITY DECISION
        # ==================================================

        if "Retreat" in self.kb.facts:

            return False

        return True


    # ======================================================
    # A* SEARCH WITH KNOWLEDGE BASE
    # ======================================================

    def astar_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size,
        food_positions=None,
        opponent_positions=None,
        toxic_traps=None
    ):

        # --------------------------------------------------
        # Safe defaults
        # --------------------------------------------------

        if food_positions is None:
            food_positions = set()

        if opponent_positions is None:
            opponent_positions = []

        if toxic_traps is None:
            toxic_traps = set()

        # ==================================================
        # A* OPEN LIST
        # ==================================================

        frontier = []

        start_h = self.manhattan_distance(
            start_pos,
            goal_pos
        )

        heapq.heappush(
            frontier,
            (
                start_h,
                0,
                start_pos,
                []
            )
        )

        # --------------------------------------------------
        # Best known g(n)
        # --------------------------------------------------

        reached = {
            start_pos: 0
        }

        # ==================================================
        # A* LOOP
        # ==================================================

        while frontier:

            (
                f_cost,
                g_cost,
                current_pos,
                path
            ) = heapq.heappop(
                frontier
            )

            # --------------------------------------------------
            # Goal Test
            # --------------------------------------------------

            if current_pos == goal_pos:

                return path

            x, y = current_pos

            # ==================================================
            # GENERATE NEIGHBOURS
            # ==================================================

            neighbours = [

                ((x, y + 1), "Up"),

                ((x, y - 1), "Down"),

                ((x - 1, y), "Left"),

                ((x + 1, y), "Right")

            ]

            # ==================================================
            # CHECK EACH NEIGHBOUR
            # ==================================================

            for next_pos, action in neighbours:

                nx, ny = next_pos

                # ==================================================
                # 1. PHYSICAL REACHABILITY
                # ==================================================

                # --------------------------------------------------
                # Boundary Check
                # --------------------------------------------------

                if nx < 0 or nx >= grid_size[0]:
                    continue

                if ny < 0 or ny >= grid_size[1]:
                    continue

                # --------------------------------------------------
                # Wall Check
                # --------------------------------------------------

                if next_pos in walls:
                    continue

                # ==================================================
                # 2. LOGICAL FEASIBILITY
                # ==================================================

                feasible = self.is_tile_feasible(
                    next_pos,
                    food_positions,
                    opponent_positions,
                    toxic_traps
                )

                # --------------------------------------------------
                # Retreat means infeasible
                # --------------------------------------------------

                if not feasible:
                    continue

                # ==================================================
                # 3. PATH COST
                # ==================================================

                new_g = g_cost + 1

                # --------------------------------------------------
                # Better path check
                # --------------------------------------------------

                if (
                    next_pos not in reached
                    or new_g < reached[next_pos]
                ):

                    reached[next_pos] = new_g

                    # ==================================================
                    # 4. HEURISTIC
                    # ==================================================

                    h = self.manhattan_distance(
                        next_pos,
                        goal_pos
                    )

                    # ==================================================
                    # 5. A* EVALUATION
                    #
                    # f(n) = g(n) + h(n)
                    # ==================================================

                    new_f = new_g + h

                    new_path = path + [action]

                    heapq.heappush(
                        frontier,
                        (
                            new_f,
                            new_g,
                            next_pos,
                            new_path
                        )
                    )

        # ==================================================
        # NO PATH EXISTS
        # ==================================================

        return None


    # ======================================================
    # AGENT DECISION
    # ======================================================

    def sense_and_act(
        self,
        percept
    ):

        # --------------------------------------------------
        # CURRENT POSITION
        # --------------------------------------------------

        current_pos = tuple(
            percept["agent_pos"]
        )

        # --------------------------------------------------
        # FOOD
        # --------------------------------------------------

        food_positions = {
            tuple(food)
            for food in percept.get(
                "all_food",
                []
            )
        }

        # --------------------------------------------------
        # WALLS
        # --------------------------------------------------

        walls = {
            tuple(wall)
            for wall in percept.get(
                "walls",
                []
            )
        }

        # --------------------------------------------------
        # GRID SIZE
        # --------------------------------------------------

        grid_size = percept.get(
            "grid_size"
        )

        # --------------------------------------------------
        # OPPONENTS
        # --------------------------------------------------

        opponent_positions = [
            tuple(op)
            for op in percept.get(
                "opponent_positions",
                []
            )
        ]

        # --------------------------------------------------
        # TOXIC TRAPS
        #
        # This now matches visual_grid_game.py
        # --------------------------------------------------

        toxic_traps = {
            tuple(trap)
            for trap in percept.get(
                "toxic_traps",
                []
            )
        }

        # ==================================================
        # NO FOOD
        # ==================================================

        if not food_positions:

            return "Stay"

        # ==================================================
        # GENERATE NEW PLAN
        # ==================================================

        if not self.current_plan:

            # --------------------------------------------------
            # Find closest food
            # --------------------------------------------------

            closest_food = min(
                food_positions,
                key=lambda food:
                    self.manhattan_distance(
                        current_pos,
                        food
                    )
            )

            goal = tuple(
                closest_food
            )

            # --------------------------------------------------
            # A* + KNOWLEDGE BASE
            # --------------------------------------------------

            self.current_plan = self.astar_search(
                current_pos,
                goal,
                walls,
                grid_size,
                food_positions,
                opponent_positions,
                toxic_traps
            )

            # --------------------------------------------------
            # No valid path
            # --------------------------------------------------

            if not self.current_plan:

                return "Stay"

        # ==================================================
        # EXECUTE FIRST ACTION
        # ==================================================

        action = self.current_plan.pop(0)

        return action


# ==========================================================
# SIMPLE OFFLINE TESTING
# ==========================================================

if __name__ == "__main__":

    agent = SearchAgent()

    start = (0, 0)

    goal = (3, 3)

    walls = {
        (1, 1),
        (2, 1)
    }

    grid_size = (4, 4)

    # ======================================================
    # BFS
    # ======================================================

    print(
        "BFS Path:",
        agent.bfs_search(
            start,
            goal,
            walls,
            grid_size
        )
    )

    # ======================================================
    # DFS
    # ======================================================

    print(
        "DFS Path:",
        agent.dfs_search(
            start,
            goal,
            walls,
            grid_size
        )
    )

    # ======================================================
    # UCS
    # ======================================================

    print(
        "UCS Path:",
        agent.ucs_search(
            start,
            goal,
            walls,
            grid_size
        )
    )

    # ======================================================
    # MANHATTAN
    # ======================================================

    print(
        "Manhattan:",
        agent.manhattan_distance(
            (0, 0),
            (3, 4)
        )
    )

    # ======================================================
    # EUCLIDEAN
    # ======================================================

    print(
        "Euclidean:",
        agent.euclidean_distance(
            (0, 0),
            (3, 4)
        )
    )

    # ======================================================
    # A*
    # ======================================================

    print(
        "A* Path:",
        agent.astar_search(
            start,
            goal,
            walls,
            grid_size
        )
    )

    # ======================================================
    # LAB 05 - KNOWLEDGE BASE TEST
    # ======================================================

    print(
        "\n--- Knowledge Base Test ---"
    )

    # ------------------------------------------------------
    # TEST 1
    # ------------------------------------------------------

    agent.kb.clear_facts()

    agent.kb.tell_fact(
        "TargetVisible"
    )

    agent.kb.tell_fact(
        "HasDust"
    )

    agent.kb.forward_chain()

    print(
        "Test 1 Facts:",
        agent.kb.facts
    )

    # ------------------------------------------------------
    # TEST 2
    # ------------------------------------------------------

    agent.kb.clear_facts()

    agent.kb.tell_fact(
        "TargetVisible"
    )

    agent.kb.tell_fact(
        "HasDust"
    )

    agent.kb.tell_fact(
        "BloodseekerMissing"
    )

    agent.kb.forward_chain()

    print(
        "Test 2 Facts:",
        agent.kb.facts
    )
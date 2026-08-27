import random
import math
from collections import deque
import heapq


class SimpleReflexAgent:

    def sense_and_act(self, percept):

        if percept["food_here"]:
            return "Stay"

        if percept["wall_ahead"]:
            return "Left"

        return "Up"


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


class SearchAgent:

    def __init__(self):

        self.active_algo = "ASTAR"
        self.current_plan = []


    # ==================================================
    # BFS
    # ==================================================

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):

        queue = deque()

        queue.append((start_pos, []))

        reached = {start_pos}

        while queue:

            current_pos, path = queue.popleft()

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

                if nx < 0 or nx >= grid_size[0]:
                    continue

                if ny < 0 or ny >= grid_size[1]:
                    continue

                if next_pos in walls:
                    continue

                if next_pos in reached:
                    continue

                reached.add(next_pos)

                new_path = path + [action]

                queue.append((next_pos, new_path))

        return None


    # ==================================================
    # DFS
    # ==================================================

    def dfs_search(self, start_pos, goal_pos, walls, grid_size):

        stack = []

        stack.append((start_pos, []))

        reached = {start_pos}

        while stack:

            current_pos, path = stack.pop()

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

                if nx < 0 or nx >= grid_size[0]:
                    continue

                if ny < 0 or ny >= grid_size[1]:
                    continue

                if next_pos in walls:
                    continue

                if next_pos in reached:
                    continue

                reached.add(next_pos)

                new_path = path + [action]

                stack.append((next_pos, new_path))

        return None


    # ==================================================
    # UCS
    # ==================================================

    def ucs_search(self, start_pos, goal_pos, walls, grid_size):

        frontier = []

        heapq.heappush(
            frontier,
            (0, start_pos, [])
        )

        reached = {
            start_pos: 0
        }

        while frontier:

            cost, current_pos, path = heapq.heappop(frontier)

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

                if nx < 0 or nx >= grid_size[0]:
                    continue

                if ny < 0 or ny >= grid_size[1]:
                    continue

                if next_pos in walls:
                    continue

                new_cost = cost + 1

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


    # ==================================================
    # MANHATTAN DISTANCE
    # ==================================================

    def manhattan_distance(self, pos1, pos2):

        return (
            abs(pos1[0] - pos2[0])
            +
            abs(pos1[1] - pos2[1])
        )


    # ==================================================
    # EUCLIDEAN DISTANCE
    # ==================================================

    def euclidean_distance(self, pos1, pos2):

        return math.sqrt(
            (pos1[0] - pos2[0]) ** 2
            +
            (pos1[1] - pos2[1]) ** 2
        )


    # ==================================================
    # A* SEARCH
    # ==================================================

    def astar_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):

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

        reached = {
            start_pos: 0
        }

        while frontier:

            f_cost, g_cost, current_pos, path = heapq.heappop(
                frontier
            )

            # Goal reached
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

                # Boundary check
                if nx < 0 or nx >= grid_size[0]:
                    continue

                if ny < 0 or ny >= grid_size[1]:
                    continue

                # Wall check
                if next_pos in walls:
                    continue

                # Actual cost
                new_g = g_cost + 1

                # Only continue if this is a better path
                if (
                    next_pos not in reached
                    or new_g < reached[next_pos]
                ):

                    reached[next_pos] = new_g

                    # Heuristic
                    h = self.manhattan_distance(
                        next_pos,
                        goal_pos
                    )

                    # A* evaluation function
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

        return None


    # ==================================================
    # AGENT DECISION
    # ==================================================

    def sense_and_act(self, percept):

        current_pos = tuple(
            percept["agent_pos"]
        )

        food_positions = percept.get(
            "all_food",
            []
        )

        walls = percept.get(
            "walls",
            []
        )

        grid_size = percept.get(
            "grid_size"
        )

        # No food left
        if not food_positions:

            return "Stay"

        # Need a new plan
        if not self.current_plan:

            # Find nearest food using Manhattan distance
            closest_food = min(
                food_positions,
                key=lambda food:
                    self.manhattan_distance(
                        current_pos,
                        tuple(food)
                    )
            )

            goal = tuple(closest_food)

            # Generate A* plan
            self.current_plan = self.astar_search(
                current_pos,
                goal,
                walls,
                grid_size
            )

            # No path found
            if not self.current_plan:

                return "Stay"

        # Execute first action in plan
        action = self.current_plan.pop(0)

        return action


# ======================================================
# SIMPLE TESTING
# ======================================================

if __name__ == "__main__":

    agent = SearchAgent()

    start = (0, 0)
    goal = (3, 3)

    walls = {
        (1, 1),
        (2, 1)
    }

    grid_size = (4, 4)

    print(
        "BFS Path:",
        agent.bfs_search(
            start,
            goal,
            walls,
            grid_size
        )
    )

    print(
        "DFS Path:",
        agent.dfs_search(
            start,
            goal,
            walls,
            grid_size
        )
    )

    print(
        "UCS Path:",
        agent.ucs_search(
            start,
            goal,
            walls,
            grid_size
        )
    )

    print(
        "Manhattan:",
        agent.manhattan_distance(
            (0, 0),
            (3, 4)
        )
    )

    print(
        "Euclidean:",
        agent.euclidean_distance(
            (0, 0),
            (3, 4)
        )
    )

    print(
        "A* Path:",
        agent.astar_search(
            start,
            goal,
            walls,
            grid_size
        )
    )
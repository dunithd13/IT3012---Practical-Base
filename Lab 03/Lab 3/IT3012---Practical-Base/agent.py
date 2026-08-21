import random
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
        
        self.plan = []
        self.active_algo = "BFS"

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        queue = deque()
        queue.append((start_pos, []))

        reached = {start_pos}

        while queue:
            current_pos, path = queue.popleft()

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

                # Check grid boundaries
                if nx < 0 or nx >= grid_size[0]:
                    continue

                if ny < 0 or ny >= grid_size[1]:
                    continue

                # Check wall
                if next_pos in walls:
                    continue

                # Check whether already visited
                if next_pos in reached:
                    continue

                reached.add(next_pos)

                new_path = path + [action]

                queue.append((next_pos, new_path))

        # No path exists
        return None

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

    def ucs_search(self, start_pos, goal_pos, walls, grid_size):
        frontier = []
        heapq.heappush(frontier, (0, start_pos, []))

        reached = {start_pos: 0}

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

                # Outside grid
                if nx < 0 or nx >= grid_size[0]:
                    continue

                if ny < 0 or ny >= grid_size[1]:
                    continue

                # Wall
                if next_pos in walls:
                    continue

                new_cost = cost + 1

                # First visit OR cheaper path
                if next_pos not in reached or new_cost < reached[next_pos]:

                    reached[next_pos] = new_cost

                    new_path = path + [action]

                    heapq.heappush(
                        frontier,
                        (new_cost, next_pos, new_path)
                    )

        return None
    


    def sense_and_act(self, percept):
        # If there are no actions left in the current plan,
        # create a new plan.
        if not self.plan:

            start_pos = tuple(percept["agent_pos"])

            food = percept["all_food"]

            if not food:
                return "Stay"

            # Select the closest food using Manhattan distance
            goal_pos = min(
                food,
                key=lambda p:
                    abs(p[0] - start_pos[0]) +
                    abs(p[1] - start_pos[1])
            )

            walls = set(tuple(w) for w in percept["walls"])
            grid_size = percept["grid_size"]

            if self.active_algo == "BFS":
                new_plan = self.bfs_search(
                    start_pos,
                    tuple(goal_pos),
                    walls,
                    grid_size
                )

            elif self.active_algo == "DFS":
                new_plan = self.dfs_search(
                    start_pos,
                    tuple(goal_pos),
                    walls,
                    grid_size
                )

            elif self.active_algo == "UCS":
                new_plan = self.ucs_search(
                    start_pos,
                    tuple(goal_pos),
                    walls,
                    grid_size
                )

            else:
                new_plan = None

            if new_plan:
                self.plan = new_plan
            else:
                return "Stay"

        # Execute one action from the plan
        return self.plan.pop(0)
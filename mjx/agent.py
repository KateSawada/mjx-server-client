import random
from typing import List

import _mjx  # type: ignore

from mjx.action import Action
from mjx.observation import Observation
from mjx.visualizer.selector import Selector


class Agent(_mjx.Agent):  # type: ignore
    def __init__(self) -> None:
        _mjx.Agent.__init__(self)  # type: ignore

    def act(self, observation: Observation) -> Action:
        raise NotImplementedError

    def act_batch(self, observations: List[Observation]) -> List[Action]:
        return [self.act(obs) for obs in observations]

    def serve(
        self,
        socket_address: str,
        batch_size: int = 64,
        wait_limit_ms: int = 100,
        sleep_ms: int = 10,
    ):
        _mjx.AgentServer(self, socket_address, batch_size, wait_limit_ms, sleep_ms)  # type: ignore

    def _act(self, observation: _mjx.Observation) -> _mjx.Action:  # type: ignore
        return self.act(Observation._from_cpp_obj(observation))._cpp_obj

    def _act_batch(self, observations: List[_mjx.Observation]) -> List[_mjx.Action]:  # type: ignore
        actions: List[Action] = self.act_batch(
            [Observation._from_cpp_obj(obs) for obs in observations]
        )
        return [action._cpp_obj for action in actions]


class RandomAgent(Agent):  # type: ignore
    def __init__(self) -> None:
        super().__init__()

    def act(self, observation: Observation) -> Action:  # type: ignore
        return random.choice(observation.legal_actions())


class RandomDebugAgent(Agent):
    def __init__(self) -> None:
        super().__init__()
        self._agent = _mjx.RandomDebugAgent()  # type: ignore

    def act(self, observation: Observation) -> Action:
        return Action._from_cpp_obj(self._act(observation._cpp_obj))

    def _act(self, observation: _mjx.Observation) -> _mjx.Action:  # type: ignore
        return self._agent._act(observation)


class RuleBasedAgent(Agent):
    def __init__(self) -> None:
        super().__init__()
        self._agent = _mjx.RuleBasedAgent()  # type: ignore

    def act(self, observation: Observation) -> Action:
        return Action._from_cpp_obj(self._act(observation._cpp_obj))

    def _act(self, observation: _mjx.Observation) -> _mjx.Action:  # type: ignore
        return self._agent._act(observation)


class HumanControlAgent(Agent):  # type: ignore
    def __init__(self, unicode: bool = False, rich: bool = False, ja: bool = False) -> None:
        super().__init__()
        self.unicode: bool = unicode
        self.ja: bool = ja
        self.rich: bool = rich

    def act(self, observation: Observation) -> Action:  # type: ignore
        return Selector.select_from_proto(
            observation.to_proto(), unicode=self.unicode, rich=self.rich, ja=self.ja
        )
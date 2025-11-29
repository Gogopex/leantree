from typing import Self

from leantree.repl_adapter.interaction import LeanProofState, LeanTactic
# TODO:
#  - running the server on a http port, managing the LeanProcessPool
#  - exposing endpoints for status and for requesting a process (with given libraries)
#  - client capable of calling endpoints on a server (has address and port)

class LeanServer:
    """Manages a LeanProcessPool and exposes it over a HTTP port."""
    pass

class LeanClient:
    """Connects to a LeanServer."""
    pass

class LeanRemoteProcess:
    def __init__(self, client: LeanClient, process_id: int):
        self.client = client
        self.process_id = process_id

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def proof_from_sorry(self, theorem_with_sorry: str) -> "RemoteLeanProofBranch":
        pass

class RemoteLeanProofBranch:
    def state(self) -> LeanProofState:
        pass

    def apply_tactic(
            self,
            tactic: LeanTactic | str,
            ban_search_tactics: bool = True,
    ) -> list[Self]:
        pass
        

def start_server(port: int):
    pass

if __name__ == "__main__":
    start_server()
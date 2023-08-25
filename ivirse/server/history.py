from dataclasses import dataclass
from typing import List, Tuple
from functools import reduce

@dataclass
class History:
    """History class for training and/or evaluation metrics collection."""
    
    def __init__(self) -> None:
        self.losses_centralized: List[Tuple[int, float]] = []
        self.acc_centralized: List[Tuple[int, float]] = []
        
    def add_loss_centralized(self, server_round: int, loss: float) -> None:
        """Add one loss entry (from centralized evaluation.)"""
        self.losses_centralized.append((server_round, loss))
        
    def add_acc_centralized(self, server_round: int, acc: float) -> None:
        """Add accuracy entry (from centralized evaluation)"""
        self.acc_centralized.append((server_round, acc))
        
    def __repr__(self) -> str:
        rep = ""
        
        if self.losses_centralized:
            rep += "History (loss, centralized):\n" + reduce(
                lambda a, b: a +  b,
                [
                    f"\tround {server_round}: {loss}\n"
                    for server_round, loss in self.losses_centralized
                ]
            )
            
        if self.acc_centralized:
            rep += "History (accuracy, centralized):\n" + reduce(
                lambda a, b: a +  b,
                [
                    f"\tround {server_round}: {acc}\n"
                    for server_round, acc in self.losses_centralized
                ]
            )
            
        return rep
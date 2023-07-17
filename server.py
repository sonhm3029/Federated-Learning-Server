from typing import Dict, List, Optional, Tuple, Union
import flwr as fl
from flwr.common import FitRes, Parameters, Scalar
from flwr.server.client_proxy import ClientProxy

import numpy as np
from flwr.server.strategy.aggregate import aggregate, weighted_loss_avg
import sys
import os

os.environ['FLWR_TELEMETRY_LOGGING'] = '1'
class CustomStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit( 
        self,
        server_round: int,
        results: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.FitRes]],
        failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
    ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:
    
        aggregated_parameters, aggregated_metrics = super().aggregate_fit(server_round, results, failures)

        return aggregated_parameters, aggregated_metrics

if __name__ == "__main__":
    fl.server.start_server(
        server_address="0.0.0.0:8000",
        config=fl.server.ServerConfig(num_rounds=4),
        strategy=CustomStrategy(
            fraction_fit=1.0,
            fraction_evaluate=1.0,
            min_fit_clients=2,
            min_evaluate_clients=2,
            min_available_clients=2,
        )
    )
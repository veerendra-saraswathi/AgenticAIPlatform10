from distributed_runtime.ray_parallel import run_agents_in_parallel

from platform10.agents.velocity_signal_agent import VelocitySignalAgent
from platform10.agents.location_signal_agent import LocationSignalAgent
from platform10.agents.vendor_risk_agent import VendorRiskAgent


def main():
    velocity_agent = VelocitySignalAgent()
    location_agent = LocationSignalAgent()
    vendor_risk_agent = VendorRiskAgent()

    results = run_agents_in_parallel([
        (velocity_agent, {"tx_count": 15}),
        (location_agent, {"country": "IN"}),
        (vendor_risk_agent, {"vendor_id": "VENDOR-123"}),
    ])

    print("PARALLEL RESULTS:")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()


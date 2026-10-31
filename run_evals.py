import asyncio
from google.adk.evaluation.agent_evaluator import AgentEvaluator


async def main():
    print("Running ADK agent evaluation...")
    await AgentEvaluator.evaluate(
        agent_module="my_agent",
        eval_dataset_file_path_or_dir="my_agent/eval_time.evalset.json",
        num_runs=1,
        print_detailed_results=True,
    )


if __name__ == "__main__":
    asyncio.run(main())


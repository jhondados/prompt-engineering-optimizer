"""DSPy-based prompt optimizer."""
import dspy
from dspy.teleprompt import MIPROv2
from typing import Callable

class PromptOptimizer:
    def __init__(self, lm_model: str = "gemini/gemini-1.5-pro-002"):
        self.lm = dspy.Google(model=lm_model, max_tokens=2048)
        dspy.settings.configure(lm=self.lm)

    def optimize(self, module: dspy.Module, trainset: list, metric: Callable,
                 num_trials: int = 50) -> dspy.Module:
        """Optimize prompts using MIPROv2 Bayesian optimization."""
        teleprompter = MIPROv2(metric=metric, num_candidates=10,
            init_temperature=1.0, verbose=True)
        optimized = teleprompter.compile(module, trainset=trainset,
            num_trials=num_trials, minibatch_size=25)
        return optimized

class QAModule(dspy.Module):
    def __init__(self): self.predict = dspy.ChainOfThought("question -> answer")
    def forward(self, question): return self.predict(question=question)

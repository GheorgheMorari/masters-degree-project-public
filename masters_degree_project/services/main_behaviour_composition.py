from masters_degree_project.adapters.llm_adapter import LLMAdapter
from masters_degree_project.domain.main_behaviour_composition_output import MainBehaviourCompositionOutput
from masters_degree_project.domain.sentence_decomposition_output import SentenceDecompositionOutput

main_behaviour_composition_instruction_template = (
    "Choose one behaviour and it's modifiers that is reflected in the main clause and compose a concise main_behaviour that represents the action in main clause."
    "main_clause: {}, behaviour_modifier_pairs: {}")


def main_behaviour_composition(sentence_decomposition_output: SentenceDecompositionOutput,
                               llm_adapter: LLMAdapter) -> MainBehaviourCompositionOutput:
    main_behaviour_composition_output = llm_adapter.generate_instruct_result(
        main_behaviour_composition_instruction_template.format(sentence_decomposition_output.main_clause,
                                                               sentence_decomposition_output.behavior_modifier_pairs),
        MainBehaviourCompositionOutput)

    return main_behaviour_composition_output

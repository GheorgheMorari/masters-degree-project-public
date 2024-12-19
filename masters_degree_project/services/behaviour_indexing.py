from masters_degree_project.adapters.llm_adapter import LLMAdapter
from masters_degree_project.services.main_behaviour_composition import main_behaviour_composition
from masters_degree_project.services.sentence_decomposition import sentence_decomposition


def behaviour_indexing(input_sentence: str, llm_adapter: LLMAdapter) -> str:
    sentence_decomposition_output = sentence_decomposition(input_sentence, llm_adapter)

    main_behaviour_composition_output = main_behaviour_composition(sentence_decomposition_output, llm_adapter)
    return main_behaviour_composition_output.main_behaviour

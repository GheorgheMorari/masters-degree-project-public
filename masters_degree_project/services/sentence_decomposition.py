from masters_degree_project.adapters.llm_adapter import LLMAdapter
from masters_degree_project.domain.sentence_decomposition_output import SentenceDecompositionOutput

sentence_decomposition_instruction_template = "Decompose the same sentence into: entities (only nouns and noun phrases), entity_modifiers (Adjectives), behaviors (only verbs and verb phrases), and behaviour_modifiers (adverbs and related phrases), and main clause:{}"


def decompose_sentence(input_sentence: str, llm_adapter: LLMAdapter) -> SentenceDecompositionOutput:
    """
    Decompose a sentence into its constituent parts using the provided LLM adapter.
    :param input_sentence: str.
    :param llm_adapter: LLMAdapter object.
    :return: str.
    """

    sentence_decomposition_output = llm_adapter.generate_instruct_result(
        sentence_decomposition_instruction_template.format(input_sentence), SentenceDecompositionOutput)

    return sentence_decomposition_output

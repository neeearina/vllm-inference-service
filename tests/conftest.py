import sys
from unittest.mock import MagicMock


def _install_fake_vllm() -> None:
    out0 = MagicMock()
    out0.text = "mocked generated text"
    out0.token_ids = [1, 2, 3]

    seq_out = MagicMock()
    seq_out.outputs = [out0]
    seq_out.prompt_token_ids = [10, 20, 30]

    mock_llm = MagicMock()
    mock_llm.generate.return_value = [seq_out]

    mock_vllm = MagicMock()
    mock_vllm.LLM = MagicMock(return_value=mock_llm)
    mock_vllm.SamplingParams = MagicMock()

    sys.modules["vllm"] = mock_vllm


_install_fake_vllm()

"""Lab config — model IDs and generation parameters."""

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

PARAMETERS = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 256,
}

CREDENTIALS = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "project_id": "skills-network",
}

# PDF uses llama-3-2-11b-vision-instruct; Skills Network IDE supports Maverick instead.
LLAMA_MODEL_ID = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"
GRANITE_MODEL_ID = "ibm/granite-4-h-small"
MISTRAL_MODEL_ID = "mistralai/mistral-small-3-1-24b-instruct-2503"
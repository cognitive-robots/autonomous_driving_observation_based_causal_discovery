# Types of Experiments
* Real World Experiments: Experiments carried out on data captured from the real world, not necessarily carried out on a live system.
* Synthetic Experiments: Experiments carried out on data generated on a computer.
* Semi-synthetic Experiments: Experiments carried out on data captured from the real world, but manipulated in such a way that the data can no longer be considered totally true to the real world.

# Structure of Experiments
* scenario: Contains the two agent convoy scenarios that causal discovery was carried out on. Data is formatted as a CSV with a column per variable.
  * raw: Scenarios with the same frame frequency as the base dataset.
  * tcdf: Scenarios resampled to 4 Hz.
  * pcmci: Scenarios resampled to 10 Hz. Unnecessary for the Lyft dataset which is at 10 Hz already.
* discovered: Causal models discovered by the observation-based approaches. Data is stored in a custom JSON format (see below).
  * rand: Causal models discovered by adding causal relationships at random.
  * tcdf: Causal models discovered by TCDF.
    * {hidden_layers}_{epochs}: The parameters utilised by TCDF to produce this set of discoveries. Not always present if only a single parameter configuration was used.
  * pcmci: Causal models discovered by PCMCI.
    * {tau_max}_{alpha}: The parameters utilised by TCDF to produce this set of discoveries. The value for alpha is multiplied by 1000 to avoid including full stops in the folder name. Not always present if only a single parameter configuration was used.
* results: Evaluation of the discoveries made by the observation-based approaches.
  * rand: Evaluation of the discoveries made by adding causal relationships at random.
  * tcdf: Evaluation of the discoveries made by TCDF.
    * {hidden_layers}_{epochs}: The parameters utilised by TCDF to produce the set of discoveries evaluated. Not always present if only a single parameter configuration was used.
  * pcmci: Evaluation of the discoveries made by PCMCI.
    * {tau_max}_{alpha}: The parameters utilised by TCDF to produce the set of discoveries evaluated. The value for alpha is multiplied by 1000 to avoid including full stops in the folder name. Not always present if only a single parameter configuration was used.
* agent_json_data: Only used for the Lyft dataset. Consists of intermediary agent data for scenes stored in a LZ4 compressed custom JSON format (this is currently not documented).

# Causal Model JSON Format
* variables: Contains the variables and their causal relationships.
  * {variable}: Information and causal relationships relevant to this particular variable.
    * parents: List of variables that are parents in a causal relationship with this variable, i.e. The listed variables have an effect on this particular variable.
* duration: Duration of the scene.
* runtime: Runtime of applying the causal discovery approach to the scene.

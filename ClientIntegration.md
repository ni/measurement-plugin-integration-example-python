# ntegrating with Custom Application - {to be changed}

## Challenges in Sequencing Measurement Plug-Ins

Imagine you have a custom application or sequencer that executes measurements. If you want to sequence or run measurement plug-ins using that custom utility, how can this be achieved?

## The Solution: Measurement Plug-In Clients

This is where the measurement plug-in clients come into the picture. It allows us to run measurements directly from a simple Python script, making it easier to invoke measurements from within a user application. This approach is highly useful for sequencing measurement plug-ins. [Know more about Measurement Plug-In Client.]({link_to_measurement_plugin_client})

### Sequence workflow using the Measurement Client Generator

Below is a visual representation of how the measurement client generator helps in sequencing measurement plug-ins.
![measurement-clients-sequence-workflow](/docs/images/measurement-clients-sequence-workflow.PNG)

The steps for integrating the measurement client generator tool with the user application have been provided in the [Measurement Client Integration](#measurement-client-integration) section.

## Gaps addressed by Measurement Client Generator

- The measurement client generator integrates seamlessly with custom applications and adapts to specific requirements.
- It allows for customizable sequence logic with user-defined inputs, providing flexibility in measurement processes.

## Measurement Client Integration

- Install the measurement client generator package:

  ```bash
  pip install ni-measurement-plugin-sdk-generator
  ```

- Import the module in your application:

  ```python
  import ni_measurement_plugin_sdk_generator.client
  ```

- Generate the measurement client using:

  ```python
  ni_measurement_plugin_sdk_generator.client.create_client.main(args=args)
  ```

    ***[View detailed argument specifications](link_for_argument_details_in_client_generator)***

   Modify the arguments based on the method's expected options or parameters.
- For better error handling, wrap method calls inside try-except blocks to catch and log exceptions:

  ```python
  try:
      ni_measurement_plugin_sdk_generator.client.create_client.main(args=args)
  except Exception as e:
      print(f"Error occurred: {e}")
  ```

## Example for Integrating the Measurement Client Generator in a Custom Sequencer

To see a practical implementation of this workflow, refer to our [Example sequencer tool.](/README.md)

# Integrating Measurement Plug-Ins with Custom applications

## Scenario: Sequencing Measurement Plug-Ins

Imagine you have a custom application or sequencer designed to execute measurements. If you want to sequence or run measurement plug-ins using this custom application, how can you leverage it to effectively sequence and execute these measurement plug-ins?

## The Solution: Measurement Plug-In Clients

Measurement plug-in clients allow you to run measurements directly from a simple Python script, simplifying the process of invoking measurements from any user application. This approach is particularly useful for sequencing multiple measurement plug-ins. [{Know more about Measurement Plug-In Client}.]({link_to_measurement_plugin_client})

### Sequencing workflow using the Measurement Plug-In Client Generator

The following visual illustrates how the Measurement Plug-In Client Generator facilitates the sequencing of measurement plug-ins.

![Measurement-clients-workflow](/docs/images/measurement-clients-workflow.PNG)

The steps for integrating the Measurement Plug-In Client Generator with a user application are outlined in the [Measurement Plug-In Client Integration](#steps-to-integrate-the-measurement-plug-in-client) section.

## Challenges Addressed by the Measurement Plug-In Client Generator

- The Measurement Plug-In Client Generator integrates seamlessly with custom applications and can be tailored to meet specific requirements.
- It enables customizable sequence logic with user-defined inputs, offering flexibility in the measurement execution.

## Steps to Integrate the Measurement Plug-In Client

- Install the Measurement Plug-In Client Generator package:

  ```bash
  pip install ni-measurement-plugin-sdk-generator
  ```

- Import the module in your application:

  ```python
  import ni_measurement_plugin_sdk_generator.client
  ```

- Use the following method to generate the measurement plug-in client(s):

  ```python
  ni_measurement_plugin_sdk_generator.client.create_client(args=args)
  ```

    ***[{View detailed argument specifications}](link_for_argument_details_in_client_generator)***

    Modify the arguments based on the method's expected options or parameters.

  **Note:** Encapsulate the call inside a `try...catch` block to handle run-time exceptions.

## Example for Integrating the Measurement Plug-In Client Generator in a Custom Sequencer

For a practical implementation of this workflow, refer to our example [Sequencer tool](/README.md).

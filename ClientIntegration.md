# Integrating Measurement Plug-Ins with User applications

You can integrate measurement plug-ins to call and execute them from user application. In this document, we will focus specifically on a **sequencer**.

## Scenario: Sequencing Measurement Plug-Ins

Imagine you have a custom application or sequencer designed to execute measurements. If you want to sequence or run measurement plug-ins using this custom application, how can you leverage it to effectively sequence and execute these measurement plug-ins?

## The Solution: Measurement Plug-In Clients

Measurement plug-in clients allow you to run measurements directly from a Python script, simplifying the process of invoking measurements from user application. [{Know more about Measurement Plug-In Client}.]({link_to_measurement_plugin_client})

The following visual illustrates how the Measurement Plug-In Client Generator can be used for calling the measurement plug-ins in user application.

![Measurement-clients-workflow](/docs/images/measurement-clients-workflow.PNG)

The steps for integrating the Measurement Plug-In Client Generator with a user application are outlined in the [Measurement Plug-In Client Integration](#steps-to-integrate-the-measurement-plug-in-client) section.

## Challenges Addressed by the Measurement Plug-In Client Generator

- The Measurement Plug-In Client Generator integrates seamlessly with custom applications and can be tailored to meet specific requirements.
- As the measure call is simple using measurement plug-in clients, it can be utilized to implement customizable sequence logic with user-defined inputs.

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

## Example for Integrating the Measurement Plug-In Client Generator in a User Application

For a practical implementation of this workflow, refer to our example [Sequencer tool](/README.md).

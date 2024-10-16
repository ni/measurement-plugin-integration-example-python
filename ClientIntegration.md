# Integrating Measurement Plug-Ins with User applications

Users can call and execute measurement plug-ins from their applications. This document focuses on a **sequencer** as the user application.

## Scenario: Sequencing Measurement Plug-Ins

Consider a user application designed to sequence and execute measurements. How can support be effectively extended to Measurement Plug-ins for this user application?

## Solution: Measurement Plug-In Clients

Measurement plug-in clients enable users to call and run measurements from a Python script, simplifying the process to invoke measurements from the user application. [{Know more about Measurement Plug-In Client}.]({link_to_measurement_plugin_client})

The following visual illustrates how the Measurement Plug-In Client Generator can be used to generate clients to invoke measurement plug-ins in the user application.

![Measurement-clients-workflow](/docs/images/measurement-clients-workflow.PNG)

An example code for integrating the Measurement Plug-In Client Generator with the user application is outlined in the [Measurement Plug-In Client Generator Integration](#example-code-to-integrate-the-measurement-plug-in-client-generator) section.

## Example code to Integrate the Measurement Plug-In Client Generator

- Install the Measurement Plug-In Client Generator package:

  ```bash
  pip install ni-measurement-plugin-sdk-generator
  ```

- Example usage:

  ```python
  import ni_measurement_plugin_sdk_generator.client

  args = [f"-s{measurement_service_class}", f"-o{output_directory}", f"-c{class_name}", f"-m{module_name}"]

  try:
      ni_measurement_plugin_sdk_generator.client.create_client(args=args)
  except Exception as e:
      raise Exception("Exception thrown from client generation: ", e)
  ```

  This can be executed in a loop to create clients for multiple measurement plug-ins.

## Example for Integrating the Measurement Plug-In Client Generator in a User Application

For a practical implementation of this workflow, refer to our example [Sequencer tool](/README.md).

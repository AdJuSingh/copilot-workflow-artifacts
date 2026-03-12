# ASW Development Instructions - VM-BS

## Application Development Standards

### Control Algorithm Development
- Use model-based design with Simulink/MATLAB
- Implement state machines for brake system modes
- Generate C code with automatic verification

### Performance Requirements
- Brake response time: < 150ms from pedal input
- System availability: 99.99% uptime
- Temperature range: -40°C to +125°C

### Testing and Validation
- Hardware-in-the-loop (HIL) testing mandatory
- Generate automated test cases for all driving scenarios
- Continuous integration with safety validation

### Integration Points
- Interface with vehicle network (CAN/Ethernet)
- Coordinate with stability control systems
- Implement fail-safe mechanisms
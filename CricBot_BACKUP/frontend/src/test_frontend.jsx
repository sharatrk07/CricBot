// test_frontend.jsx
import { render, screen, fireEvent } from "@testing-library/react";
import App from "../App";

describe("CricBot Frontend Tests", () => {
  test("renders CricBot header", () => {
    render(<App />);
    const headerElement = screen.getByText(/CricBot/i);
    expect(headerElement).toBeInTheDocument();
  });

  test("sends a message and displays user message", () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Type your message.../i);
    const sendButton = screen.getByText(/Send/i);
    fireEvent.change(inputElement, { target: { value: "Hello" } });
    fireEvent.click(sendButton);
    expect(screen.getByText("Hello")).toBeInTheDocument();
  });
});
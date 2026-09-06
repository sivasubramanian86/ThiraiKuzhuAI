import "@testing-library/jest-dom";

// Mock EventSource for SSE testing
class MockEventSource {
  constructor(url) {
    this.url = url;
    this.readyState = 0;
    this.onopen = null;
    this.onmessage = null;
    this.onerror = null;
    this.listeners = {};
    setTimeout(() => {
      this.readyState = 1;
      if (this.onopen) this.onopen({ type: "open" });
    }, 0);
  }
  addEventListener(event, callback) {
    this.listeners[event] = callback;
  }
  removeEventListener(event, callback) {
    if (this.listeners[event] === callback) {
      delete this.listeners[event];
    }
  }
  close() {
    this.readyState = 2;
  }
}

global.EventSource = MockEventSource;

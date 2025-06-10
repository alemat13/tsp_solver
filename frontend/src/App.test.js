import { render, screen } from '@testing-library/react';
import App from './App';

// Mock Map component to avoid React Leaflet dependency issues in Jest
jest.mock('./components/Map', () => () => <div />);

test('renders the main heading', () => {
  render(<App />);
  const headingElement = screen.getByText(/Optimize GPS Positions/i);
  expect(headingElement).toBeInTheDocument();
});

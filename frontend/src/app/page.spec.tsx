import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import Home from './page';
import React from 'react';

type Article = {
    header: string;
    url: string;
};

const mock = new MockAdapter(axios);

describe('Home Component', () => {
    beforeEach(() => {
        mock.reset();
    });

    it('renders the component correctly', () => {
        render(<Home />);
        expect(screen.getByText('News Article Search')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Enter keywords separated by comma')).toBeInTheDocument();
        expect(screen.getByText('Search')).toBeInTheDocument();
    });

    it('updates the input value on change', () => {
        render(<Home />);
        const input = screen.getByPlaceholderText('Enter keywords separated by comma') as HTMLInputElement;
        fireEvent.change(input, { target: { value: 'test,react' } });
        expect(input.value).toBe('test,react');
    });

    it('fetches articles and displays them on successful search', async () => {
        const articles: Article[] = [
            { header: 'Test Article 1', url: 'http://example.com/1' },
            { header: 'Test Article 2', url: 'http://example.com/2' },
        ];

        mock.onPost('http://localhost:5000/articles/find').reply(200, { articles });

        render(<Home />);
        const input = screen.getByPlaceholderText('Enter keywords separated by comma') as HTMLInputElement;
        fireEvent.change(input, { target: { value: 'test' } });
        fireEvent.click(screen.getByText('Search'));

        await waitFor(() => expect(screen.getByText('Test Article 1')).toBeInTheDocument());
        expect(screen.getByText('Test Article 2')).toBeInTheDocument();
    });

    it('displays an error message on server error', async () => {
        mock.onPost('http://localhost:5000/articles/find').reply(500);

        render(<Home />);
        const input = screen.getByPlaceholderText('Enter keywords separated by comma') as HTMLInputElement;
        fireEvent.change(input, { target: { value: 'test' } });
        fireEvent.click(screen.getByText('Search'));

        await waitFor(() => expect(screen.getByText('Internal server error. Please try again later.')).toBeInTheDocument());
    });

    it('displays an error message on network error', async () => {
        mock.onPost('http://localhost:5000/articles/find').networkError();

        render(<Home />);
        const input = screen.getByPlaceholderText('Enter keywords separated by comma') as HTMLInputElement;
        fireEvent.change(input, { target: { value: 'test' } });
        fireEvent.click(screen.getByText('Search'));

        await waitFor(() => expect(screen.getByText('Failed to fetch articles. Please try again later.')).toBeInTheDocument());
    });

    it('displays an error message on unexpected error', async () => {
        mock.onPost('http://localhost:5000/articles/find').reply(() => {
            throw new Error('Unexpected error');
        });

        render(<Home />);
        const input = screen.getByPlaceholderText('Enter keywords separated by comma') as HTMLInputElement;
        fireEvent.change(input, { target: { value: 'test' } });
        fireEvent.click(screen.getByText('Search'));

        await waitFor(() => expect(screen.getByText('An unexpected error occurred. Please try again later.')).toBeInTheDocument());
    });
});

# SHL Coding Assignment for Software Developer(AI)

## Task and Tech-Stack Used

- Build an end-to-end application - both backend and frontend.
- Using Next.js for frontend and Django(Python) for Backend.
- Using Tailwind CSS for styling.
- Using SQLite database (for better portability).
- Integration process of PostGreSQL/MySQL database is similar.

## Backend

- Read a file containing the details extracted from a sample of 100 projects.
- Load this information into a database.
- Implement backend APIs to access this data on front-end.
- Use GPT for smart search functionality.

## Frontend

- Build a responsive application.
- Show the information in the form of Gallery/Tiles.
- Build a list view where user can explore a given project in detail,looking at all the parameters.
- Search option for specific projects.
  - Smart search functionality with the help of GPT-3.5/4 where one can do multi-attribute search. For ex, find me projects where ReactJS is used in front-end, and Python is used in backend.

## Environment Variables in Backend

The Django Backend uses two environment variables in a `.env` file inside the `projectBackend` directory. The variables are:

```bash
SECRET_KEY=<django_secret_key>
OPENAI_API_KEY=<your_openai_api_key>
```

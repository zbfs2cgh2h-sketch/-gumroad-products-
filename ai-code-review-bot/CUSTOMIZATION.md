# Example: Customize Reviews for Your Tech Stack

## Python/Django Project

Edit `prompts/review-prompt.txt` and add:

```
## Django-Specific Checks
- N+1 query problems (use select_related/prefetch_related)
- Missing database indexes on filtered fields
- Unvalidated user input in views
- Missing CSRF protection on forms
- Improper use of Q objects
```

## React/TypeScript Project

```
## React-Specific Checks
- Missing dependency arrays in useEffect/useCallback/useMemo
- Unnecessary re-renders (use React.memo, useMemo)
- Props not typed properly
- State mutations instead of immutable updates
- Missing error boundaries
- Accessibility (missing aria labels, alt text)
```

## Go Project

```
## Go-Specific Checks
- Goroutines without proper error handling
- Missing context cancellation
- defer in loops (resource leak)
- Errors not properly wrapped
- Missing interface documentation
```

## Rust Project

```
## Rust-Specific Checks
- Unnecessary use of unsafe blocks
- Clone calls that could be references
- Missing error propagation (?)
- Unwrap/expect in production code
- Missing lifetime annotations where needed
```

## API Security Checklist

```
## API-Specific Checks
- Missing rate limiting
- No authentication on sensitive endpoints
- Returning sensitive data in error messages
- Missing input validation
- CORS misconfiguration
- Missing API versioning strategy
```

---

After editing, commit the changes and the bot will use your custom rules on the next PR.

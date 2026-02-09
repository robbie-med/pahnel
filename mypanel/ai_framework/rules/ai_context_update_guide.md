# Feature Context Management Guide

## When Context Updates Are Needed

Hegemon Framework is designed to NOT require frequent context updates. However, certain major project changes might benefit from updates to AI_PROJ_CONTEXT.md:

### Events That Might Trigger Updates

1. **Technology Stack Changes**
   - New framework adoption
   - Database migration
   - Major dependency updates

2. **Architecture Shifts**
   - Monolith → Microservices
   - REST → GraphQL
   - Sync → Async

3. **New Patterns Established**
   - Custom error handling
   - Specific naming conventions
   - Project-specific utilities

## Manual Update Process

When significant changes occur, update AI_PROJ_CONTEXT.md:

```markdown
## Recent Changes (Updated: YYYY-MM-DD)

### New Technology Stack
- Migrated from Express to Fastify
- Added Redis for caching
- Integrated Stripe for payments

### New Patterns
- All services use dependency injection
- Error codes follow pattern: MODULE_ERROR_DESCRIPTION
- All async operations use Promise.allSettled()
```

## Why We Don't Auto-Update

1. **Stability**: AI_CONTEXT.md remains stable across all features
2. **Clarity**: PROJECT_DIRECTIVES.md is explicitly managed
3. **Control**: Human decides what context changes matter
4. **Simplicity**: No complex bash scripts to maintain

## Best Practices

### DO
- Update PROJECT_DIRECTIVES.md after major architecture decisions
- Document new patterns as they emerge
- Keep updates concise and actionable

### DON'T
- Update for every small feature
- Duplicate information already in specs
- Auto-generate context changes

## Example PROJECT_DIRECTIVES.md Update

```markdown
# Project-Specific AI Directives

## Stack (Updated: 2024-01-15)
- TypeScript 5.3 with strict mode
- Next.js 14 with App Router
- Prisma ORM with PostgreSQL
- tRPC for type-safe APIs

## Patterns (Updated: 2024-01-20)
- Server components by default
- Client components only for interactivity
- All database queries through repository pattern
- Use Zod for runtime validation

## Recent Decisions (Updated: 2024-01-25)
- Migrated auth from NextAuth to Clerk
- All new features must have E2E tests
- Using Turborepo for monorepo management
```

## Integration with Specs

Each FEAT-XXX spec already contains its own context:
- Technology choices
- Patterns to follow
- Dependencies

The AI reads these specs when implementing that specific feature. No need to pollute global context.

## Conclusion

Hegemon's approach:
- **Global context** (AI_CONTEXT.md) = Framework rules
- **Project context** (PROJECT_DIRECTIVES.md) = Project-wide patterns
- **Feature context** (specs/FEAT-XXX/) = Feature-specific details

This separation keeps context minimal and relevant!
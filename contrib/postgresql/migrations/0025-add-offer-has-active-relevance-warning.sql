ALTER TABLE offers
    ADD COLUMN has_active_relevance_warning bool not null default false;

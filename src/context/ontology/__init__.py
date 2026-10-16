from pydantic import BaseModel, Field


class Customer(BaseModel):
    """A company that buys (or bought) Orbisa or Brisklane products."""

    plan: str | None = Field(None, description="Starter, Growth or Enterprise")
    contract_paper: str | None = Field(None, description="Orbisa standard terms, an Orbisa MSA, or Brisklane legacy terms")
    lifecycle: str | None = Field(None, description="Customer, at risk, or former customer")


class Person(BaseModel):
    """An employee of Orbisa or Brisklane, or a contact person at a customer. Merge aliases and nicknames of the same person."""

    job_title: str | None = Field(None, description="Job title, for example Head of RevOps")
    employer: str | None = Field(None, description="Company the person works for")


class Team(BaseModel):
    """An internal team or function, such as Finance, RevOps, Support or Data Platform."""


class Policy(BaseModel):
    """A written company rule: refund, SLA and service credit, discount approval, or data retention."""

    policy_id: str | None = Field(None, description="Policy identifier such as POL-007")
    version: str | None = Field(None, description="Policy version")
    effective_date: str | None = Field(None, description="Date the policy takes effect, YYYY-MM-DD")


class Contract(BaseModel):
    """A signed agreement between Orbisa and a customer: MSA, order form or addendum."""

    contract_number: str | None = Field(None, description="Order form or agreement number")
    annual_fee: str | None = Field(None, description="Annual subscription fee with currency")
    renewal_date: str | None = Field(None, description="Next renewal date, YYYY-MM-DD")


class Plan(BaseModel):
    """A subscription plan sold by Orbisa or by Brisklane."""

    price: str | None = Field(None, description="List price")


class Incident(BaseModel):
    """A production incident or outage of an Orbisa service."""

    incident_id: str | None = Field(None, description="Incident identifier such as INC-2291")
    duration: str | None = Field(None, description="How long the incident lasted")


class Product(BaseModel):
    """An Orbisa product such as Orbisa Track or Orbisa Bill."""


ENTITY_TYPES: dict[str, type[BaseModel]] = {
    "Customer": Customer,
    "Person": Person,
    "Team": Team,
    "Policy": Policy,
    "Contract": Contract,
    "Plan": Plan,
    "Incident": Incident,
    "Product": Product,
}
